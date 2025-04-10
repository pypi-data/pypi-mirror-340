"""
AI integration for Arrow Cache MCP.

This module provides integration with AI models, particularly Anthropic's Claude.
"""

import os
import re
import time
import logging
import json
from typing import Dict, List, Optional, Tuple, Any, Union

from .core import get_arrow_cache

# Configure logging
logger = logging.getLogger(__name__)

# Try to import anthropic
try:
    import anthropic
    HAVE_ANTHROPIC = True
except ImportError:
    HAVE_ANTHROPIC = False
    logger.warning("Anthropic library not installed. Claude functionality will be limited.")

def get_claude_api_key() -> Optional[str]:
    """
    Get the Claude API key from environment variable or other configuration.
    
    Returns:
        API key or None if not found
    """
    # Try to get from env var first
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    # If not in env var, check if it's stored elsewhere in your configuration
    if not api_key:
        # Implement additional sources if needed
        pass
        
    return api_key

def extract_and_run_queries(claude_response: str) -> Tuple[str, List[str], List[Dict[str, Any]], bool]:
    """
    Extract SQL queries from Claude's response, execute them, and add the results.
    
    Args:
        claude_response: Text response from Claude
        
    Returns:
        Tuple of (processed_response, executed_queries, results_data, error_occurred)
    """
    # Get the cache
    cache = get_arrow_cache()
    
    parts = []
    current_pos = 0
    executed_queries = []  # Track executed queries
    results_data = []  # Store query results for potential followup
    error_occurred = False  # Track if any errors occurred
    
    # Look for query blocks
    while True:
        query_start = claude_response.find("<query>", current_pos)
        if query_start == -1:
            # Add the remaining text
            if current_pos < len(claude_response):
                parts.append(claude_response[current_pos:])
            break
            
        # Add text before the query
        if query_start > current_pos:
            parts.append(claude_response[current_pos:query_start])
            
        query_end = claude_response.find("</query>", query_start)
        if query_end == -1:
            # Malformed response, just add everything
            parts.append(claude_response[current_pos:])
            break
            
        # Extract the query
        query = claude_response[query_start + 8:query_end].strip()
        executed_queries.append(query)  # Add to executed queries list
        
        # Execute the query
        try:
            # Use the query optimizer for better performance
            try:
                from arrow_cache.query_optimization import explain_query
                
                # Extract table references using the optimizer's method
                if hasattr(cache.query_optimizer, '_extract_table_references'):
                    table_refs = cache.query_optimizer._extract_table_references(query)
                    if table_refs:
                        # Ensure these tables are registered before explaining
                        cache._ensure_tables_registered(table_refs)
                        logger.info(f"Ensured tables {table_refs} are registered before explaining.")
                
                # Get query plan explanation for insights
                explanation = explain_query(cache.metadata_store.con, query)
                query_plan_info = explanation
            except Exception as explain_e:
                logger.warning(f"Error getting query plan explanation: {explain_e}")
                query_plan_info = f"Query plan explanation failed: {explain_e}"
            
            start_time = time.time()
            
            # Execute the query using cache's internal optimization
            result_df = cache.query(query, optimize=True)
            query_time = time.time() - start_time
            
            # Convert Arrow table to pandas DataFrame for easier display
            # (PyArrow Tables don't have to_markdown method)
            if hasattr(result_df, 'to_pandas'):
                pandas_df = result_df.to_pandas()
            else:
                pandas_df = result_df  # In case it's already a DataFrame
            
            # Store the results and query plan for potential followup
            results_data.append({
                "query": query, 
                "result_df": pandas_df,
                "query_time": query_time,
                "query_plan": query_plan_info
            })
            
            # Format results
            parts.append("\n\n**Query:**\n```sql\n")
            parts.append(query)
            parts.append("\n```\n\n")
            parts.append(f"*Query executed in {query_time:.3f}s*\n\n")
            parts.append("**Results:**\n\n")
            
            # Convert DataFrame to markdown table for better rendering
            # For smaller results, convert to markdown
            if len(pandas_df) < 10 and len(pandas_df.columns) < 8:
                try:
                    # Use pandas markdown format if available
                    parts.append(pandas_df.to_markdown(index=False))
                except (AttributeError, ImportError):
                    # Fallback if to_markdown is not available
                    parts.append(str(pandas_df))
            else:
                # For larger results, provide a message about the size
                parts.append(f"*Showing {len(pandas_df)} rows with {len(pandas_df.columns)} columns.*\n\n")
                # Add a sample of the data
                parts.append(pandas_df.head(5).to_string())
                parts.append("\n\n*...more rows...*\n\n")
                
        except Exception as e:
            error_occurred = True
            error_message = str(e)
            
            # Provide more helpful error messages for common issues
            if "Table with name _cache_" in str(e) and "does not exist" in str(e):
                # Extract table name from error message
                import re
                table_name_match = re.search(r"_cache_(\w+)", str(e))
                if table_name_match:
                    table_name = table_name_match.group(1)
                    available_tables = cache.get_keys() 
                    error_message = f"Table '{table_name}' not found. Available tables: {', '.join(available_tables)}"
            
            # Format error
            parts.append("\n\n**Query:**\n```sql\n")
            parts.append(query)
            parts.append("\n```\n\n**Error:** ")
            parts.append(error_message)
            parts.append("\n\n")
            
            # Store error info for potential followup
            results_data.append({"query": query, "error": error_message, "query_time": 0})
            
        current_pos = query_end + 8  # Move past </query>
    
    return "".join(parts), executed_queries, results_data, error_occurred

def ask_claude(question: str, api_key: str, conversation_history: Optional[List[Dict[str, Any]]] = None) -> str:
    """
    Ask Claude a question about the datasets in the cache.
    
    Args:
        question: Question to ask
        api_key: Claude API key
        conversation_history: Optional conversation history
        
    Returns:
        Claude's response
    """
    if not api_key:
        return "Error: Anthropic API key not found. Please set the ANTHROPIC_API_KEY environment variable."
        
    if not HAVE_ANTHROPIC:
        return "Error: Anthropic library not installed. Please install it with: pip install anthropic"
    
    # Initialize conversation history if not provided
    if conversation_history is None:
        conversation_history = []
    
    # Add the user question to the history
    conversation_history.append({
        "role": "user",
        "content": question,
        "timestamp": time.time()
    })
    
    # Get datasets info for context with enhanced metadata
    cache = get_arrow_cache()
    datasets = []
    try:
        from .core import get_datasets_list
        datasets = get_datasets_list()
    except Exception as e:
        logger.error(f"Error getting datasets list: {e}")
    
    datasets_info = ""
    for ds in datasets:
        # Basic dataset info
        datasets_info += f"\n- Dataset '{ds['name']}': {ds.get('row_count', 'Unknown')} rows, {len(ds.get('columns', []))} columns"
        
        # Add format information if available
        if 'format' in ds:
            datasets_info += f"\n  Format: {ds['format']}"
            
        # Add source information if available
        if 'source' in ds:
            datasets_info += f"\n  Source: {ds['source']}"
        
        # Add column details with data types
        if 'columns' in ds and 'dtypes' in ds:
            datasets_info += "\n  Columns with data types:"
            for col in ds['columns']:
                dtype = ds['dtypes'].get(col, 'unknown')
                datasets_info += f"\n    - {col}: {dtype}"
        elif 'columns' in ds:
            datasets_info += f"\n  Columns: {', '.join(ds['columns'])}"
            
        # Add additional stats if available
        if 'memory_bytes' in ds:
            datasets_info += f"\n  Memory usage: {ds['memory_bytes'] / (1024*1024):.2f} MB"
            
        # Add any other metadata that would be useful for Claude
        if 'metadata' in ds:
            for key, value in ds['metadata'].items():
                if key not in ['columns', 'dtypes', 'format', 'source', 'row_count'] and not key.startswith('_'):
                    datasets_info += f"\n  {key}: {value}"
    
    client = anthropic.Anthropic(api_key=api_key)
    
    # Include conversation history context for the system prompt
    conversation_context = ""
    if len(conversation_history) > 1:
        # Include last few exchanges for context if this isn't the first message
        last_exchanges = conversation_history[-3:]  # Last 3 exchanges
        conversation_context = "Recent conversation history:\n"
        for entry in last_exchanges:
            if entry["role"] == "user":
                conversation_context += f"User: {entry['content']}\n"
            else:
                # Just include the text part without the query results for context
                content = entry["content"]
                if "query_executed" in entry:
                    # If there was a query, add a note about it
                    conversation_context += f"Claude: [Answered and ran query: {entry['query_executed']}]\n"
                else:
                    conversation_context += f"Claude: [Provided answer without query]\n"
    
    # Build the context and prompt
    system_prompt = f"""
    You are a data analyst with access to a data sandbox containing multiple datasets.
    The following datasets are currently available in the cache:
    {datasets_info}
    
    IMPORTANT QUERY INSTRUCTIONS:
    - When querying a dataset, ALWAYS use the FROM clause syntax: FROM _cache_<dataset_name>
    - ALWAYS verify the dataset name exists in the list above before using it in a query
    - The dataset name in _cache_<dataset_name> must EXACTLY match one of the dataset names listed above
    - If you're unsure if a dataset exists, ONLY use datasets explicitly listed above
    - Double-check column names before using them in queries
    
    {conversation_context}
    
    Your task is to help the user analyze these datasets by:
    1. Whenever possible, use the dataset metadata I've provided to answer simple questions without running a query
    2. For more complex analysis, generate appropriate SQL queries 
    3. Generate ONLY DuckDB-compatible SQL queries
    4. Include the query within <query> tags
    
    Important SQL syntax notes for DuckDB:
    - Tables are accessed with _cache_ prefix: FROM _cache_<dataset_name>
    - Case sensitivity: Table and column names are case-sensitive
    - WITH clauses must be at the beginning of the query
    - Each CTE must have a name followed by AS and then a subquery in parentheses
    - Multiple CTEs must be separated by commas
    - DuckDB supports standard SQL functions like SUM, AVG, COUNT, etc.
    - For dates, use functions like DATE_TRUNC, EXTRACT, etc.
    - Use single quotes for string literals: WHERE column = 'value'
    
    Example correct query:
    <query>
    SELECT 
      column1, 
      SUM(column2) AS total,
      AVG(column3) AS average
    FROM _cache_dataset_name
    WHERE column4 = 'value'
    GROUP BY column1
    ORDER BY total DESC
    LIMIT 10;
    </query>
    """
    
    try:
        # STEP 1: Call the Claude API to get query
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            temperature=0,
            system=system_prompt,
            messages=[
                {"role": "user", "content": question}
            ]
        )
        
        initial_response = message.content[0].text
        
        # Extract and execute any SQL queries in the response
        response_with_results, executed_queries, results_data, error_occurred = extract_and_run_queries(initial_response)
        
        # STEP 2: If queries were executed, ask Claude to interpret the results
        if results_data:
            # Prepare result information for Claude
            query_result_info = ""
            for idx, data in enumerate(results_data):
                query = data["query"]
                
                if "error" in data:
                    # Handle error case
                    error_message = data["error"]
                    query_result_info += f"\nQuery {idx+1}:\n{query}\n\nError: {error_message}\n"
                    
                else:
                    # Handle successful query
                    result_df = data["result_df"]
                    
                    # Convert DataFrame to string representation for Claude
                    if len(result_df) > 10:
                        # If large result, provide summary of first 10 rows
                        result_str = f"First 10 rows out of {len(result_df)} total rows:\n{result_df.head(10).to_string()}"
                    else:
                        # If small result, provide all rows
                        result_str = result_df.to_string()
                    
                    query_result_info += f"\nQuery {idx+1}:\n{query}\n\nResults:\n{result_str}\n"
            
            # Create a follow-up prompt for Claude to interpret results
            followup_system_prompt = f"""
            You are a data analyst with access to a data sandbox containing multiple datasets.
            
            I ran the SQL query you provided, and I need you to analyze the results.
            
            Rules for your response:
            1. Provide a clear, accurate interpretation based ONLY on the actual data in the query results
            2. Use precise values from the results - exact numbers, formats, and data types
            3. Highlight key patterns, trends, or notable outliers in the data
            4. Never make up values or predict data that isn't in the results
            5. Keep your analysis focused on what the data actually shows
            
            {f'''
            ERROR CORRECTION INSTRUCTIONS:
            The query had errors. Please:
            1. Identify the specific error in the original query
            2. Provide a corrected query that should work
            3. Explain the correction you made
            
            Common errors to check for:
            - Incorrect table name (check if the dataset exists exactly as referenced)
            - Column name errors (check spelling and case)
            - SQL syntax errors (check keywords, operators, quotes, etc.)
            - Type mismatches (e.g., comparing string to number)
            ''' if error_occurred else ''}
            
            The query and its results are provided below:
            {query_result_info}
            """
            
            # Get Claude's interpretation of the results
            followup_message = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                temperature=0,
                system=followup_system_prompt,
                messages=[
                    {"role": "user", "content": "Please interpret these query results accurately." + (" If there were SQL errors, please provide a corrected query." if error_occurred else "")}
                ]
            )
            
            interpretation_response = followup_message.content[0].text
            
            # Combine the original query with the interpretation
            final_response = response_with_results + "\n\n**Interpretation:**\n" + interpretation_response
        else:
            # If no queries were executed, just use the original response
            final_response = response_with_results
        
        # Add Claude's response to the history with query info
        history_entry = {
            "role": "assistant",
            "content": final_response,
            "timestamp": time.time(),
        }
        
        # Add query information if queries were executed
        if executed_queries:
            history_entry["query_executed"] = executed_queries[0] if executed_queries else None
            history_entry["query_count"] = len(executed_queries)
            if error_occurred:
                history_entry["error_occurred"] = True
        
        conversation_history.append(history_entry)
        
        return final_response
    except Exception as e:
        error_message = f"Error connecting to Claude API: {str(e)}"
        logger.error(error_message)
        # Add error to conversation history
        conversation_history.append({
            "role": "system",
            "content": error_message,
            "timestamp": time.time()
        })
        return error_message

def display_conversation_history(conversation_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Format conversation history for display.
    
    Args:
        conversation_history: List of conversation entries
        
    Returns:
        Formatted conversation data
    """
    if not conversation_history:
        return []
    
    formatted_history = []
    for entry in conversation_history:
        formatted_entry = {
            "role": entry["role"],
            "content": entry["content"],
            "timestamp": entry["timestamp"]
        }
        
        # Add query information if available
        if "query_executed" in entry:
            formatted_entry["query_executed"] = entry["query_executed"]
        if "query_count" in entry:
            formatted_entry["query_count"] = entry["query_count"]
        if "error_occurred" in entry:
            formatted_entry["error_occurred"] = entry["error_occurred"]
            
        formatted_history.append(formatted_entry)
        
    return formatted_history

def add_clear_history_button() -> None:
    """
    Add a button to clear the conversation history.
    
    This is a no-op in this context - each MCP client has its own way to handle this.
    """
    # This function exists for compatibility with the original data_mcp.py
    # In the MCP context, clearing history would be handled by the client
    pass 