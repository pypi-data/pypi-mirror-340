"""
Overview module for quick data exploration and summary.
"""
import pandas as pd
import numpy as np


def quick_look(df, name="DataFrame", include_describe=True, include_info=True):
    """
    Provides a comprehensive overview of a DataFrame.

    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    name : str, default="DataFrame"
        Name to display for the DataFrame.
    include_describe : bool, default=True
        Whether to include the describe() output.
    include_info : bool, default=True
        Whether to include the info() output.

    Returns:
    -------
    dict
        Dictionary containing summary statistics and information about the DataFrame.
    """
    summary = {}
    summary["name"] = name
    summary["shape"] = df.shape
    summary["columns"] = list(df.columns)
    summary["dtypes"] = df.dtypes.to_dict()
    summary["missing_values"] = df.isnull().sum().to_dict()
    summary["missing_percentage"] = (df.isnull().mean() * 100).to_dict()
    summary["unique_values"] = df.nunique().to_dict()
    
    # Print the summary
    print("=" * 50)
    print(f"Quick Look: {name}")
    print("=" * 50)
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\nData Types:")
    print(df.dtypes)
    print("\nMissing Values:")
    print(df.isnull().sum())
    print("\nMissing Percentage:")
    print((df.isnull().mean() * 100).round(2).astype(str) + '%')
    print("\nUnique Values:")
    print(df.nunique())
    print("\nHead:")
    print(df.head())
    print("\nTail:")
    print(df.tail())
    
    if include_describe:
        print("\nDescribe:")
        print(df.describe())
        summary["describe"] = df.describe().to_dict()
    
    if include_info:
        print("\nInfo:")
        df.info()
    
    print("=" * 50)
    
    return summary


def get_duplicates(df, subset=None, keep='first'):
    """
    Find and return duplicate rows in a DataFrame.

    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    subset : str or list, optional
        Column name or list of column names to consider for identifying duplicates.
        If None, all columns are considered.
    keep : {'first', 'last', False}, default='first'
        Determines which duplicates (if any) to mark:
            - 'first': Mark duplicates except for the first occurrence.
            - 'last' : Mark duplicates except for the last occurrence.
            - False  : Mark all duplicates.

    Returns:
    -------
    pandas.DataFrame
        A DataFrame containing the duplicate rows based on the specified columns.

    Example:
    -------
    >>> get_duplicates(df, subset=['item_name', 'quantity'], keep=False)
    """
    try:
        # Check if subset columns exist in the DataFrame
        if subset is not None:
            if isinstance(subset, str):
                subset = [subset]
            missing_cols = [col for col in subset if col not in df.columns]
            if missing_cols:
                print(f"Warning: Columns {missing_cols} not found in DataFrame.")
                print(f"Available columns: {df.columns.tolist()}")
                return df.head(0)  # Return empty DataFrame with same structure
        
        # Find duplicates
        duplicates = df[df.duplicated(subset=subset, keep=keep)].copy()
        
        # Reset index for better readability
        duplicates.reset_index(drop=True, inplace=True)
        
        # Print summary
        if len(duplicates) > 0:
            print(f"Found {len(duplicates)} duplicate rows based on {subset if subset else 'all columns'}.")
        else:
            print(f"No duplicates found based on {subset if subset else 'all columns'}.")
            
        return duplicates
    
    except Exception as e:
        print(f"Error finding duplicates: {e}")
        return df.head(0)  # Return empty DataFrame with same structure


def value_counts_all(df, top_n=5):
    """
    Returns top N frequent values for all object/categorical columns.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    top_n : int, default=5
        Number of top values to return for each column.
        
    Returns:
    -------
    dict
        Dictionary with column names as keys and DataFrames of value counts as values.
        Each DataFrame contains the top N values and their counts for that column.
    
    Example:
    -------
    >>> result = value_counts_all(df, top_n=3)
    >>> for col, counts in result.items():
    ...     print(f"\n{col}:")
    ...     print(counts)
    """
    # Select only object and categorical columns
    obj_cols = df.select_dtypes(include=['object', 'category']).columns
    
    if len(obj_cols) == 0:
        print("No object or categorical columns found in the DataFrame.")
        return {}
    
    # Dictionary to store results
    result = {}
    
    # Calculate value counts for each column
    for col in obj_cols:
        # Get value counts
        counts = df[col].value_counts(dropna=False).reset_index()
        counts.columns = [col, 'count']
        
        # Calculate percentage
        counts['percentage'] = (counts['count'] / len(df) * 100).round(2)
        counts['percentage'] = counts['percentage'].astype(str) + '%'
        
        # Get top N values
        top_counts = counts.head(top_n)
        
        # Add to result dictionary
        result[col] = top_counts
    
    # Print summary
    print(f"Top {top_n} values for {len(obj_cols)} object/categorical columns:")
    for col, counts in result.items():
        print(f"\n{col}:")
        print(counts)
    
    return result


def plot_value_counts(df, columns=None, top_n=5, figsize=(12, 8)):
    """
    Plot bar charts of value counts for specified categorical columns.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    columns : list or None, default=None
        List of column names to plot. If None, all object/categorical columns are used.
    top_n : int, default=5
        Number of top values to display for each column.
    figsize : tuple, default=(12, 8)
        Figure size as (width, height) in inches.
        
    Returns:
    -------
    matplotlib.figure.Figure
        The figure containing the plots.
    
    Example:
    -------
    >>> plot_value_counts(df, columns=['Category', 'Status'], top_n=3)
    """
    import matplotlib.pyplot as plt
    import numpy as np
    
    # Select columns to plot
    if columns is None:
        # Use all object and categorical columns
        columns = df.select_dtypes(include=['object', 'category']).columns
    else:
        # Filter out non-existent columns
        columns = [col for col in columns if col in df.columns]
        # Filter out non-object/non-categorical columns
        obj_cols = df.select_dtypes(include=['object', 'category']).columns
        columns = [col for col in columns if col in obj_cols]
    
    if len(columns) == 0:
        print("No valid object or categorical columns found to plot.")
        return None
    
    # Determine subplot grid dimensions
    n_cols = min(2, len(columns))  # Max 2 columns in the grid
    n_rows = (len(columns) + n_cols - 1) // n_cols
    
    # Create figure and subplots
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    if n_rows * n_cols == 1:  # If only one subplot, axes is not a list
        axes = np.array([axes])
    axes = axes.flatten()
    
    # Plot each column
    for i, col in enumerate(columns):
        ax = axes[i]
        
        # Get value counts
        counts = df[col].value_counts(dropna=False).reset_index()
        counts.columns = [col, 'count']
        
        # Calculate percentage
        counts['percentage'] = (counts['count'] / len(df) * 100).round(2)
        
        # Get top N values
        top_counts = counts.head(top_n)
        
        # Create horizontal bar chart
        bars = ax.barh(top_counts[col].astype(str), top_counts['count'], color='skyblue')
        
        # Add count and percentage labels
        for j, bar in enumerate(bars):
            width = bar.get_width()
            percentage = top_counts['percentage'].iloc[j]
            label = f"{width} ({percentage}%)"
            ax.text(width + (max(top_counts['count']) * 0.02), bar.get_y() + bar.get_height()/2, 
                   label, va='center')
        
        # Set title and labels
        ax.set_title(f'Top {top_n} values for {col}')
        ax.set_xlabel('Count')
        ax.set_ylabel(col)
        
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Add grid lines
        ax.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Hide unused subplots
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)
    
    plt.tight_layout()
    plt.show()
    
    return fig


def column_info(df, column=None):
    """
    Provides detailed information about a specific column or all columns.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    column : str or None, default=None
        Column name to analyze. If None, analyzes all columns.
        
    Returns:
    -------
    dict
        Dictionary containing detailed information about the column(s).
    """
    if column is not None and column not in df.columns:
        print(f"Column '{column}' not found in DataFrame.")
        print(f"Available columns: {df.columns.tolist()}")
        return {}
    
    columns_to_analyze = [column] if column else df.columns
    result = {}
    
    for col in columns_to_analyze:
        col_info = {}
        col_info["dtype"] = str(df[col].dtype)
        col_info["count"] = len(df[col])
        col_info["missing"] = df[col].isnull().sum()
        col_info["missing_percentage"] = round(df[col].isnull().mean() * 100, 2)
        col_info["unique_values"] = df[col].nunique()
        
        # Add type-specific information
        if pd.api.types.is_numeric_dtype(df[col]):
            col_info["min"] = df[col].min()
            col_info["max"] = df[col].max()
            col_info["mean"] = df[col].mean()
            col_info["median"] = df[col].median()
            col_info["std"] = df[col].std()
            
            # Check for zeros and negative values
            col_info["zeros"] = (df[col] == 0).sum()
            col_info["zeros_percentage"] = round((df[col] == 0).mean() * 100, 2)
            col_info["negative_values"] = (df[col] < 0).sum()
            col_info["negative_percentage"] = round((df[col] < 0).mean() * 100, 2)
            
        elif pd.api.types.is_string_dtype(df[col]) or pd.api.types.is_categorical_dtype(df[col]):
            # Get most common values
            value_counts = df[col].value_counts(dropna=False)
            if not value_counts.empty:
                col_info["most_common"] = value_counts.index[0]
                col_info["most_common_count"] = value_counts.iloc[0]
                col_info["most_common_percentage"] = round(value_counts.iloc[0] / len(df) * 100, 2)
            
            # Check for empty strings
            if pd.api.types.is_string_dtype(df[col]):
                empty_strings = (df[col] == "").sum()
                col_info["empty_strings"] = empty_strings
                col_info["empty_strings_percentage"] = round(empty_strings / len(df) * 100, 2)
        
        elif pd.api.types.is_datetime64_dtype(df[col]):
            col_info["min_date"] = df[col].min()
            col_info["max_date"] = df[col].max()
            col_info["range_days"] = (df[col].max() - df[col].min()).days
        
        result[col] = col_info
        
        # Print the information
        print(f"\n{'=' * 40}")
        print(f"Column: {col}")
        print(f"{'=' * 40}")
        for key, value in col_info.items():
            print(f"{key}: {value}")
    
    return result


def find_outliers(df, columns=None, method='iqr', threshold=1.5):
    """
    Find outliers in numeric columns using different methods.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    columns : list or None, default=None
        List of column names to check for outliers. If None, all numeric columns are used.
    method : str, default='iqr'
        Method to use for outlier detection:
        - 'iqr': Interquartile Range method
        - 'zscore': Z-score method
        - 'std': Standard Deviation method
    threshold : float, default=1.5
        Threshold for outlier detection:
        - For 'iqr': Values outside Q1 - threshold*IQR and Q3 + threshold*IQR are outliers
        - For 'zscore': Values with absolute Z-score > threshold are outliers
        - For 'std': Values outside mean ± threshold*std are outliers
        
    Returns:
    -------
    dict
        Dictionary with column names as keys and DataFrames of outliers as values.
    """
    from scipy import stats
    
    # Select columns to analyze
    if columns is None:
        columns = df.select_dtypes(include=['number']).columns
    else:
        # Filter out non-existent columns
        columns = [col for col in columns if col in df.columns]
        # Filter out non-numeric columns
        num_cols = df.select_dtypes(include=['number']).columns
        columns = [col for col in columns if col in num_cols]
    
    if len(columns) == 0:
        print("No valid numeric columns found for outlier detection.")
        return {}
    
    result = {}
    summary = {}
    
    for col in columns:
        # Skip columns with all missing values
        if df[col].isnull().all():
            continue
        
        # Get non-missing values
        values = df[col].dropna()
        
        # Find outliers based on the selected method
        if method == 'iqr':
            Q1 = values.quantile(0.25)
            Q3 = values.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            
            summary[col] = {
                'method': 'IQR',
                'Q1': Q1,
                'Q3': Q3,
                'IQR': IQR,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'outlier_count': len(outliers),
                'outlier_percentage': round(len(outliers) / len(df) * 100, 2)
            }
            
        elif method == 'zscore':
            z_scores = stats.zscore(values)
            abs_z_scores = np.abs(z_scores)
            filtered_entries = (abs_z_scores > threshold)
            outlier_indices = values.index[filtered_entries]
            outliers = df.loc[outlier_indices]
            
            summary[col] = {
                'method': 'Z-score',
                'threshold': threshold,
                'outlier_count': len(outliers),
                'outlier_percentage': round(len(outliers) / len(df) * 100, 2)
            }
            
        elif method == 'std':
            mean = values.mean()
            std = values.std()
            lower_bound = mean - threshold * std
            upper_bound = mean + threshold * std
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            
            summary[col] = {
                'method': 'Standard Deviation',
                'mean': mean,
                'std': std,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'outlier_count': len(outliers),
                'outlier_percentage': round(len(outliers) / len(df) * 100, 2)
            }
            
        else:
            print(f"Invalid method: {method}. Using 'iqr' instead.")
            Q1 = values.quantile(0.25)
            Q3 = values.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            
            summary[col] = {
                'method': 'IQR',
                'Q1': Q1,
                'Q3': Q3,
                'IQR': IQR,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'outlier_count': len(outliers),
                'outlier_percentage': round(len(outliers) / len(df) * 100, 2)
            }
        
        result[col] = outliers
    
    # Print summary
    print(f"Outlier Detection Summary (method: {method}, threshold: {threshold}):")
    for col, info in summary.items():
        print(f"\n{col}:")
        for key, value in info.items():
            print(f"  {key}: {value}")
    
    return result
