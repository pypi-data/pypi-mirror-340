"""
Visualization functions for Arrow Cache MCP.

This module provides functions to create visualizations from cached datasets.
"""

import io
import base64
import logging
from typing import Dict, List, Optional, Tuple, Any, Union

import pandas as pd
import matplotlib.pyplot as plt

from .core import get_arrow_cache
from .utils import get_size_display

# Configure logging
logger = logging.getLogger(__name__)

# Default plotting parameters
DEFAULT_PLOT_DPI = 100

def create_plot(dataset_name: str, x: str, y: Optional[str] = None, 
                kind: str = 'line', **kwargs) -> Tuple[Optional[str], str]:
    """
    Create a plot from a dataset and return as base64 image.
    
    Args:
        dataset_name: Name of the dataset
        x: Column name for x-axis
        y: Column name(s) for y-axis
        kind: Type of plot ('line', 'bar', 'scatter', 'hist', etc.)
        **kwargs: Additional arguments to pass to the plotting function
        
    Returns:
        Tuple of (base64_encoded_image, message)
    """
    cache = get_arrow_cache()
    
    if not cache.contains(dataset_name):
        return None, f"Dataset '{dataset_name}' not found."
    
    try:
        # Get data (limit rows for plotting)
        df = cache.get(dataset_name, limit=10000)
        
        # Check columns exist
        if x not in df.columns:
            return None, f"Column '{x}' not found in dataset '{dataset_name}'."
        
        if y and isinstance(y, str) and y not in df.columns:
            return None, f"Column '{y}' not found in dataset '{dataset_name}'."
        
        if y and isinstance(y, list):
            for col in y:
                if col not in df.columns:
                    return None, f"Column '{col}' not found in dataset '{dataset_name}'."
        
        # Extract dpi parameter for savefig (not for plot function)
        dpi = kwargs.pop('dpi', DEFAULT_PLOT_DPI) if 'dpi' in kwargs else DEFAULT_PLOT_DPI
        
        # Create plot
        plt.figure(figsize=kwargs.get('figsize', (10, 6)))
        
        plot_func = getattr(df.plot, kind)
        ax = plot_func(x=x, y=y, **kwargs)
        fig = ax.get_figure()
        
        # Set title if provided
        if 'title' in kwargs:
            plt.title(kwargs['title'])
        
        # Save to buffer as PNG with dpi parameter
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=dpi)
        buf.seek(0)
        
        # Convert to base64
        plot_base64 = base64.b64encode(buf.read()).decode('utf-8')
        
        # Clean up
        plt.close(fig)
        
        return plot_base64, "Plot created successfully."
    
    except Exception as e:
        import traceback
        logger.error(traceback.format_exc())
        return None, f"Error creating plot: {str(e)}"

def render_dataset_card(dataset: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prepare a dataset card with its info for display.
    
    Args:
        dataset: Dataset information dictionary
        
    Returns:
        Dictionary with formatted dataset info
    """
    # Get size information
    size_bytes = dataset.get('size_bytes', 0)
    size_display = get_size_display(size_bytes)
    
    # Format row count with commas for readability
    row_count = dataset.get('row_count', 'Unknown')
    if isinstance(row_count, int) or (isinstance(row_count, str) and row_count.isdigit()):
        row_count = f"{int(row_count):,}"
    
    # Get column information
    column_count = dataset.get('column_count', len(dataset.get('columns', [])))
    
    # Format metadata for display
    metadata = {}
    
    # Add format info if available
    if 'format' in dataset:
        metadata['format'] = dataset['format']
        
    # Add source if available (truncated for display)
    if 'source' in dataset:
        source = dataset['source']
        if len(source) > 50:
            source = source[:47] + "..."
        metadata['source'] = source
        
    # Add created time if available
    if 'created_at' in dataset:
        from datetime import datetime
        created_time = datetime.fromtimestamp(dataset['created_at']).strftime("%Y-%m-%d %H:%M")
        metadata['created_at'] = created_time
    
    # Prepare column preview
    columns_preview = []
    if 'columns' in dataset and dataset['columns']:
        # First try to get column types from metadata if available
        if 'dtypes' in dataset and isinstance(dataset['dtypes'], dict):
            # Display columns with their types
            for col in dataset['columns'][:20]:  # Limit to 20 columns
                dtype = dataset['dtypes'].get(col, '').replace('DataType', '')
                columns_preview.append({"name": col, "type": dtype})
        else:
            # Just list column names
            columns_preview = [{"name": col} for col in dataset['columns'][:20]]
            
        # Add indicator if there are more columns
        if len(dataset['columns']) > 20:
            columns_preview.append({"name": "...", "type": f"(plus {len(dataset['columns']) - 20} more)"})
    
    # Prepare result
    result = {
        "name": dataset['name'],
        "size": size_display,
        "size_bytes": size_bytes,
        "row_count": row_count,
        "column_count": column_count,
        "metadata": metadata,
        "columns": columns_preview,
    }
    
    # Add geospatial info if applicable
    if dataset.get('is_geospatial'):
        result["is_geospatial"] = True
        if "crs" in dataset:
            result["crs"] = dataset["crs"]
        if "geometry_column" in dataset:
            result["geometry_column"] = dataset["geometry_column"]
    
    return result 