"""
Data loading functions for Arrow Cache MCP.

This module provides functions to load datasets from various sources.
"""

import os
import time
import tempfile
import logging
import pyarrow as pa
import pandas as pd
import urllib.request
from typing import Dict, List, Optional, Tuple, Any, Union
from urllib.parse import urlparse

from .core import get_arrow_cache
from .utils import clean_dataset_name

# Configure logging
logger = logging.getLogger(__name__)

# Supported file formats
SUPPORTED_FORMATS = {
    'csv': {'extensions': ['.csv']},
    'parquet': {'extensions': ['.parquet', '.pq']},
    'arrow': {'extensions': ['.arrow', '.feather']},
    'feather': {'extensions': ['.feather']},
    'json': {'extensions': ['.json']},
    'excel': {'extensions': ['.xlsx', '.xls']},
}

# Try to import optional geospatial dependencies
try:
    import geopandas as gpd
    SUPPORTED_FORMATS['geojson'] = {'extensions': ['.geojson']}
    SUPPORTED_FORMATS['geoparquet'] = {'extensions': ['.geoparquet']}
    HAS_GEOPANDAS = True
except ImportError:
    HAS_GEOPANDAS = False
    logger.warning("GeoPandas not installed. Geospatial formats won't be available.")

def guess_format_from_path(file_path: str) -> Optional[str]:
    """
    Guess the format of a file based on its extension.
    
    Args:
        file_path: Path or URL to the file
        
    Returns:
        Format name or None if unknown
    """
    # Extract just the filename from path or URL
    if '://' in file_path:  # It's a URL
        parsed_url = urlparse(file_path)
        file_path = os.path.basename(parsed_url.path)
    
    ext = os.path.splitext(file_path.lower())[1]
    if not ext:
        return None
        
    for format_name, format_info in SUPPORTED_FORMATS.items():
        if ext in format_info['extensions']:
            return format_name
            
    # If we get here, the extension wasn't recognized
    return None

def load_dataset_from_path(path: str, dataset_name: Optional[str] = None, 
                           format: Optional[str] = None, **kwargs) -> Tuple[bool, Union[Dict[str, Any], str]]:
    """
    Load a dataset from a local path into the cache.
    
    Args:
        path: Path to the dataset file
        dataset_name: Name to assign to the dataset (defaults to filename)
        format: Format of the dataset (autodetected if None)
        **kwargs: Additional arguments to pass to the reader
        
    Returns:
        Tuple of (success, result_or_error_message)
    """
    cache = get_arrow_cache()
    
    if not dataset_name:
        # Extract name from path (remove extension)
        base_name = os.path.basename(path).split('.')[0]
        # Clean up name
        dataset_name = clean_dataset_name(base_name)
    
    # Check if dataset with this name already exists
    if cache.contains(dataset_name):
        return False, f"Dataset '{dataset_name}' already exists. Please use a different name or remove it first."
    
    # Determine format if not provided
    if not format:
        # Try using arrow_cache.converters for format detection
        try:
            from arrow_cache.converters import guess_format
            format = guess_format(path)
            logger.info(f"Format detection from converters: {format}")
        except (ImportError, Exception) as e:
            logger.error(f"Error using converter's format detection: {e}")
            # Fall back to our own detection
            format = guess_format_from_path(path)
        
        if not format:
            return False, f"Could not determine format from file extension. Please specify it explicitly."
    
    if format not in SUPPORTED_FORMATS:
        return False, f"Unsupported format: {format}. Supported formats: {list(SUPPORTED_FORMATS.keys())}"
    
    try:
        # Special case for yellow taxi dataset which has partitioning issues
        if "yellow_tripdata" in path and format == "parquet":
            logger.info(f"Detected NYC yellow taxi dataset. Using Arrow-native direct loading approach.")
            
            # Custom parameters for reading the taxi dataset to prevent over-partitioning
            config_dict = cache.config.to_dict()
            config_dict.update({
                'partition_size_rows': 5000000,  # Force much larger rows per partition 
                'partition_size_bytes': 500 * 1024 * 1024,  # Force larger partition size (500MB)
                'dictionary_encoding': False,  # Completely disable dictionary encoding
                'enable_compression': False,  # Disable compression for initial load
            })
            
            from arrow_cache import ArrowCacheConfig
            custom_config = ArrowCacheConfig(**config_dict)
            
            # Use Arrow-native loading with memory mapping for performance
            import pyarrow.parquet as pq
            start_time = time.time()
            
            # Use memory mapping and direct table read without any transformations
            table = pq.read_table(
                path, 
                use_threads=True,
                memory_map=True,
                use_pandas_metadata=False
            )
            load_time = time.time() - start_time
            
            # Use ArrowCache's built-in size estimation instead of custom calculation
            from arrow_cache.converters import estimate_size_bytes
            size_bytes = estimate_size_bytes(table)
            
            # Prepare metadata
            metadata = {
                'source': path,
                'format': format,
                'loaded_at': time.time(),
                'load_time_seconds': load_time,
                'row_count': table.num_rows,
                'column_count': len(table.column_names),
                'columns': list(table.column_names),
                'dtypes': {col: str(table.schema.field(col).type) for col in table.column_names},
                'custom_loading': 'Used fully native Arrow loading without dictionary encoding or compression',
                'raw_data': True,  # Flag that this is raw data with no transformations
                'memory_bytes': size_bytes,
                'size_bytes': size_bytes
            }
            
            # Store with custom config
            start_cache_time = time.time()
            # Force replacement of config temporarily
            original_config = cache.config
            cache.config = custom_config
            
            try:
                # Use built-in partitioning functionality from cache.py and partitioning.py
                from arrow_cache.partitioning import partition_table
                
                # Let Arrow Cache handle partitioning decisions based on config
                if table.num_rows > custom_config["partition_size_rows"]:
                    logger.info(f"Table size ({table.num_rows} rows) exceeds partition size threshold, using partitioning")
                    cache.put(dataset_name, table, metadata=metadata, auto_partition=True)
                else:
                    # For smaller tables, use normal put without partitioning
                    cache.put(dataset_name, table, metadata=metadata, auto_partition=False)
            finally:
                # Restore original config
                cache.config = original_config
                
            cache_time = time.time() - start_cache_time
            
            # Update metadata with timing info
            metadata['cache_time_seconds'] = cache_time
            metadata['total_time_seconds'] = load_time + cache_time
            metadata['name'] = dataset_name
            
            return True, metadata
            
        # Regular case for other files
        start_time = time.time()
        
        # Use arrow_cache.converters for direct Arrow conversion when possible
        try:
            from arrow_cache.converters import to_arrow_table, estimate_size_bytes
            
            # Check if this format is directly supported by converters
            if format in ['parquet', 'arrow', 'feather', 'csv', 'json']:
                logger.info(f"Using arrow_cache.converters.to_arrow_table for {format}")
                # Pass through kwargs for CSV options etc.
                try:
                    # Try our new safe converter first
                    from arrow_cache.threading import safe_to_arrow_table
                    table = safe_to_arrow_table(path, preserve_index=True, **kwargs)
                except ImportError:
                    # Fall back to direct call if safe_to_arrow_table isn't available yet
                    table = to_arrow_table(path, preserve_index=True)
                load_time = time.time() - start_time
                
                # Prepare metadata using Arrow info
                size_bytes = estimate_size_bytes(table)
                
                metadata = {
                    'source': path,
                    'format': format,
                    'loaded_at': time.time(),
                    'load_time_seconds': load_time,
                    'row_count': table.num_rows,
                    'column_count': len(table.column_names),
                    'columns': list(table.column_names),
                    'memory_bytes': size_bytes,
                    'size_bytes': size_bytes,
                    'dtypes': {col: str(table.schema.field(col).type) for col in table.column_names},
                    'converted_by': 'arrow_cache.converters.to_arrow_table'
                }
                
                # Store the Arrow table directly
                start_cache_time = time.time()
                cache.put(dataset_name, table, metadata=metadata, 
                         auto_partition=cache.config["auto_partition"])
                cache_time = time.time() - start_cache_time
                
                # Update metadata with timing info
                metadata['cache_time_seconds'] = cache_time
                metadata['total_time_seconds'] = load_time + cache_time
                metadata['name'] = dataset_name
                
                return True, metadata
        except (ImportError, Exception) as e:
            logger.error(f"Direct conversion failed, falling back to pandas: {e}")
        
        # Fall back to pandas-based loading for other formats
        # Load the dataset based on format
        if format == 'csv':
            df = pd.read_csv(path, **kwargs)
        elif format == 'parquet':
            df = pd.read_parquet(path, **kwargs)
        elif format == 'arrow' or format == 'feather':
            df = pd.read_feather(path, **kwargs)
        elif format == 'json':
            df = pd.read_json(path, orient="records", **kwargs)
        elif format == 'excel':
            df = pd.read_excel(path, **kwargs)
        elif format == 'geojson' and HAS_GEOPANDAS:
            df = gpd.read_file(path, **kwargs)
        elif format == 'geoparquet' and HAS_GEOPANDAS:
            df = gpd.read_parquet(path, **kwargs)
        else:
            return False, f"Unsupported format: {format}"
            
        load_time = time.time() - start_time
        
        # Get dataframe memory usage
        df_memory = df.memory_usage(deep=True).sum()
        
        # Prepare metadata
        metadata = {
            'source': path,
            'format': format,
            'loaded_at': time.time(),
            'load_time_seconds': load_time,
            'row_count': len(df),
            'column_count': len(df.columns),
            'columns': list(df.columns),
            'memory_bytes': int(df_memory),
            'size_bytes': int(df_memory),
            'dtypes': {str(col): str(dtype) for col, dtype in df.dtypes.items()},
            'converted_by': 'pandas'
        }
        
        # Add geospatial metadata if applicable
        if hasattr(df, 'crs') and df.crs is not None:
            metadata['is_geospatial'] = True
            metadata['crs'] = str(df.crs)
            if hasattr(df, 'geometry'):
                metadata['geometry_column'] = 'geometry'
        
        # Let ArrowCache optimize the conversion and storage
        try:
            # Use ArrowCache's preferred storage method
            # The cache's put method will handle the conversion and optimization
            start_cache_time = time.time()
            cache.put(dataset_name, df, metadata=metadata, 
                     auto_partition=cache.config["auto_partition"])
            cache_time = time.time() - start_cache_time
        except Exception as cache_error:
            # If ArrowCache's put method fails, try the direct approach
            logger.error(f"Error using ArrowCache's put method: {cache_error}. Trying direct approach.")
            # Convert to Arrow table directly 
            import pyarrow as pa
            try:
                arrow_table = pa.Table.from_pandas(df)
                start_cache_time = time.time()
                cache.put(dataset_name, arrow_table, metadata=metadata, 
                         auto_partition=cache.config["auto_partition"])
                cache_time = time.time() - start_cache_time
            except Exception as arrow_error:
                return False, f"Error storing dataset: {arrow_error}"
        
        # Update metadata with timing info
        metadata['cache_time_seconds'] = cache_time
        metadata['total_time_seconds'] = load_time + cache_time
        
        # Add dataset name to metadata so it can be accessed in success messages
        metadata['name'] = dataset_name
        
        return True, metadata
    
    except Exception as e:
        import traceback
        logger.error(traceback.format_exc())
        return False, f"Error loading dataset: {str(e)}"

def load_dataset_from_upload(uploaded_file: Any, dataset_name: Optional[str] = None, 
                            format: Optional[str] = None, **kwargs) -> Tuple[bool, Union[Dict[str, Any], str]]:
    """
    Load a dataset from an uploaded file into the cache.
    
    Args:
        uploaded_file: File-like object with getvalue() method
        dataset_name: Name to assign to the dataset (defaults to filename)
        format: Format of the dataset (autodetected if None)
        **kwargs: Additional arguments to pass to the reader
        
    Returns:
        Tuple of (success, result_or_error_message)
    """
    if not dataset_name:
        base_name = uploaded_file.name.split('.')[0]
        # Clean up name
        dataset_name = clean_dataset_name(base_name)
    
    # Check if dataset already exists
    cache = get_arrow_cache()
    if cache.contains(dataset_name):
        return False, f"Dataset '{dataset_name}' already exists. Please use a different name or remove it first."
    
    # Save uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{uploaded_file.name}") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        temp_path = tmp_file.name
    
    try:
        # Now load from the temporary file
        success, result = load_dataset_from_path(temp_path, dataset_name, format, **kwargs)
        # Clean up temp file
        os.unlink(temp_path)
        return success, result
    except Exception as e:
        # Clean up temp file even on error
        try:
            os.unlink(temp_path)
        except:
            pass
        return False, f"Error loading uploaded file: {str(e)}"

def load_dataset_from_url(url: str, dataset_name: Optional[str] = None, 
                         format: Optional[str] = None, **kwargs) -> Tuple[bool, Union[Dict[str, Any], str]]:
    """
    Load a dataset from a URL into the cache.
    
    Args:
        url: URL of the dataset file
        dataset_name: Name to assign to the dataset (defaults to filename)
        format: Format of the dataset (autodetected if None)
        **kwargs: Additional arguments to pass to the reader
        
    Returns:
        Tuple of (success, result_or_error_message)
    """
    if not dataset_name:
        # Extract name from URL
        path = urlparse(url).path
        base_name = os.path.basename(path).split('.')[0]
        # Clean up name
        dataset_name = clean_dataset_name(base_name)
    
    # Check if dataset already exists
    cache = get_arrow_cache()
    if cache.contains(dataset_name):
        return False, f"Dataset '{dataset_name}' already exists. Please use a different name or remove it first."
    
    try:
        # Download to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            logger.info(f"Downloading from {url}...")
            urllib.request.urlretrieve(url, tmp_file.name)
            temp_path = tmp_file.name
        
        # Now load from the temporary file
        success, result = load_dataset_from_path(temp_path, dataset_name, format, **kwargs)
        # Clean up temp file
        os.unlink(temp_path)
        
        # Ensure dataset name is in the result
        if success and isinstance(result, dict) and 'name' not in result:
            result['name'] = dataset_name
            
        return success, result
    except Exception as e:
        # Clean up temp file even on error
        try:
            os.unlink(temp_path)
        except:
            pass
        return False, f"Error downloading or loading from URL: {str(e)}" 