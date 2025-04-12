"""
Data types module for handling and converting data types.
"""
import pandas as pd
import numpy as np


def to_numeric_cols(df, columns):
    """
    Convert specified DataFrame column(s) to numeric type.

    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    columns : str or list
        Column name or list of column names to convert.

    Returns:
    -------
    pandas.DataFrame
        DataFrame with specified columns converted to numeric type.
    """
    if isinstance(columns, str):
        columns = [columns]

    result = df.copy()
    for col in columns:
        if col in df.columns:
            # Store original values for comparison
            original_values = df[col].copy()
            
            # Convert to numeric
            result[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Count conversions and NaN values
            converted_count = len(result[col].dropna())
            nan_count = result[col].isna().sum() - original_values.isna().sum()
            
            # Print summary
            if nan_count > 0:
                print(f"Column '{col}': Converted {converted_count} values to numeric. {nan_count} values could not be converted and were set to NaN.")
            else:
                print(f"Column '{col}': Successfully converted all values to numeric.")
        else:
            print(f"Column '{col}' not found in DataFrame.")

    return result


def to_datetime_cols(df, cols=None):
    """
    Convert specified DataFrame column(s) to datetime type.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    cols : str or list
        Column name or list of column names to convert.

    Returns:
    -------
    pandas.DataFrame
        DataFrame with specified columns converted to datetime type.
    """
    if isinstance(cols, str):
        cols = [cols]
    
    result = df.copy()
    for col in cols:
        if col in df.columns:
            # Store original values for comparison
            original_values = df[col].copy()
            
            # Convert to datetime
            result[col] = pd.to_datetime(df[col], errors='coerce')
            
            # Count conversions and NaN values
            converted_count = len(result[col].dropna())
            nan_count = result[col].isna().sum() - original_values.isna().sum()
            
            # Print summary
            if nan_count > 0:
                print(f"Column '{col}': Converted {converted_count} values to datetime. {nan_count} values could not be converted and were set to NaN.")
            else:
                print(f"Column '{col}': Successfully converted all values to datetime.")
        else:
            print(f"Column '{col}' not found in DataFrame.")
    
    return result


def to_category_cols(df, cols=None, min_unique=10, max_unique_ratio=0.1):
    """
    Convert specified DataFrame column(s) to category type.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    cols : str, list, or None
        Column name or list of column names to convert.
        If None, automatically detect categorical columns.
    min_unique : int, default=10
        Minimum number of unique values for auto-detection.
    max_unique_ratio : float, default=0.1
        Maximum ratio of unique values to total values for auto-detection.

    Returns:
    -------
    pandas.DataFrame
        DataFrame with specified columns converted to category type.
    """
    result = df.copy()
    
    # Auto-detect categorical columns if cols is None
    if cols is None:
        cols = []
        for col in df.columns:
            # Skip numeric and datetime columns
            if pd.api.types.is_numeric_dtype(df[col]) or pd.api.types.is_datetime64_any_dtype(df[col]):
                continue
            
            # Check if column has few unique values
            n_unique = df[col].nunique()
            if n_unique >= min_unique and n_unique / len(df) <= max_unique_ratio:
                cols.append(col)
    elif isinstance(cols, str):
        cols = [cols]
    
    # Convert columns to category
    for col in cols:
        if col in df.columns:
            result[col] = result[col].astype('category')
            print(f"Column '{col}': Converted to category type with {result[col].cat.categories.size} categories.")
        else:
            print(f"Column '{col}' not found in DataFrame.")
    
    return result


def infer_dtypes(df, convert=True):
    """
    Infer and optionally convert data types for all columns in a DataFrame.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    convert : bool, default=True
        Whether to convert columns to inferred types.

    Returns:
    -------
    pandas.DataFrame or dict
        If convert=True, returns DataFrame with converted types.
        If convert=False, returns dictionary with column names and inferred types.
    """
    inferred_types = {}
    result = df.copy() if convert else None
    
    for col in df.columns:
        # Try numeric conversion
        numeric_series = pd.to_numeric(df[col], errors='coerce')
        numeric_conversion = numeric_series.notna().mean()
        
        # Try datetime conversion
        datetime_series = pd.to_datetime(df[col], errors='coerce')
        datetime_conversion = datetime_series.notna().mean()
        
        # Check for categorical
        n_unique = df[col].nunique()
        unique_ratio = n_unique / len(df) if len(df) > 0 else 1
        
        # Determine best type
        if numeric_conversion > 0.8:
            inferred_types[col] = 'numeric'
            if convert:
                result[col] = numeric_series
        elif datetime_conversion > 0.8:
            inferred_types[col] = 'datetime'
            if convert:
                result[col] = datetime_series
        elif unique_ratio <= 0.1 and n_unique >= 2:
            inferred_types[col] = 'category'
            if convert:
                result[col] = df[col].astype('category')
        else:
            inferred_types[col] = 'object'
            if convert:
                result[col] = df[col].astype('object')
    
    # Print summary
    print("Inferred data types:")
    for col, dtype in inferred_types.items():
        print(f"- {col}: {dtype}")
    
    return result if convert else inferred_types


def memory_usage(df, deep=True):
    """
    Calculate memory usage of a DataFrame and suggest optimizations.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    deep : bool, default=True
        Whether to perform a deep introspection of memory usage.

    Returns:
    -------
    dict
        Dictionary with memory usage information.
    """
    # Calculate current memory usage
    current_usage = df.memory_usage(deep=deep).sum()
    
    # Create optimized copy for comparison
    optimized_df = df.copy()
    
    # Optimize numeric columns
    int_cols = df.select_dtypes(include=['int']).columns
    for col in int_cols:
        # Find min and max values
        col_min = df[col].min()
        col_max = df[col].max()
        
        # Determine smallest possible integer type
        if col_min >= 0:
            if col_max < 2**8:
                optimized_df[col] = df[col].astype(np.uint8)
            elif col_max < 2**16:
                optimized_df[col] = df[col].astype(np.uint16)
            elif col_max < 2**32:
                optimized_df[col] = df[col].astype(np.uint32)
            else:
                optimized_df[col] = df[col].astype(np.uint64)
        else:
            if col_min > -2**7 and col_max < 2**7:
                optimized_df[col] = df[col].astype(np.int8)
            elif col_min > -2**15 and col_max < 2**15:
                optimized_df[col] = df[col].astype(np.int16)
            elif col_min > -2**31 and col_max < 2**31:
                optimized_df[col] = df[col].astype(np.int32)
            else:
                optimized_df[col] = df[col].astype(np.int64)
    
    # Optimize float columns
    float_cols = df.select_dtypes(include=['float']).columns
    for col in float_cols:
        # Check if float32 is sufficient
        optimized_df[col] = df[col].astype(np.float32)
    
    # Optimize object columns with few unique values
    object_cols = df.select_dtypes(include=['object']).columns
    for col in object_cols:
        n_unique = df[col].nunique()
        if n_unique / len(df) < 0.5:  # If less than 50% unique values
            optimized_df[col] = df[col].astype('category')
    
    # Calculate optimized memory usage
    optimized_usage = optimized_df.memory_usage(deep=deep).sum()
    
    # Prepare results
    results = {
        'original_size': current_usage,
        'optimized_size': optimized_usage,
        'savings': current_usage - optimized_usage,
        'savings_percentage': (1 - optimized_usage / current_usage) * 100 if current_usage > 0 else 0,
        'column_dtypes': {col: str(df[col].dtype) for col in df.columns},
        'optimized_dtypes': {col: str(optimized_df[col].dtype) for col in optimized_df.columns}
    }
    
    # Print summary
    print(f"Original memory usage: {current_usage / 1e6:.2f} MB")
    print(f"Optimized memory usage: {optimized_usage / 1e6:.2f} MB")
    print(f"Memory savings: {results['savings'] / 1e6:.2f} MB ({results['savings_percentage']:.2f}%)")
    
    # Print detailed optimization suggestions
    print("\nOptimization suggestions:")
    for col in df.columns:
        if str(df[col].dtype) != str(optimized_df[col].dtype):
            print(f"- Convert '{col}' from {df[col].dtype} to {optimized_df[col].dtype}")
    
    return results, optimized_df
