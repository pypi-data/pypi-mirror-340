"""
Exploratory Data Analysis module for data exploration and visualization.
"""
import pandas as pd
import numpy as np


def check_skew(df, cols=None):
    """
    Print skewness of selected columns.

    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    cols : str, list, or None
        Column(s) to check for skewness.
        If string, checks that single column.
        If list, checks all columns in the list.
        If None, checks all numeric columns.
    """
    from scipy.stats import skew
    
    # Handle different input types for cols
    if cols is None:
        # Use all numeric columns
        cols = df.select_dtypes(include='number').columns
    elif isinstance(cols, str):
        # Convert single column name to a list
        cols = [cols]
    elif not isinstance(cols, (list, pd.Index)):
        raise TypeError("'cols' must be a string, list, pandas.Index, or None")
    
    # Check if specified columns exist in the DataFrame
    missing_cols = [col for col in cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Columns not found in DataFrame: {missing_cols}")
    
    print("\n" + "=" * 30)
    print("Skewness Analysis")
    print("=" * 30)
    
    for col in cols:
        # Check if column is numeric
        if df[col].dtype.kind not in 'iufc':
            print(f"{col}: Not a numeric column (type: {df[col].dtype})")
            continue
            
        # Calculate skewness
        val = skew(df[col].dropna())
        print(f"{col}: skew = {val:.4f}")
        
        # Interpret skewness
        if abs(val) < 0.5:
            interpretation = "approximately symmetric"
        elif abs(val) < 1.0:
            interpretation = "moderately skewed"
        else:
            interpretation = "highly skewed"
            
        # Direction of skew
        direction = "positively" if val > 0 else "negatively"
        if abs(val) >= 0.5:
            print(f"   → {direction} {interpretation}")
        else:
            print(f"   → {interpretation}")
    
    print("=" * 30)
    
    return None


def plot_skew(df, cols=None, bins=30, figsize=(12, 8)):
    """
    Plot histograms to visualize the skewness of selected columns.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    cols : str, list, or None
        Column(s) to visualize.
        If string, plots that single column.
        If list, plots all columns in the list.
        If None, plots all numeric columns (up to 9 columns).
    bins : int, default=30
        Number of bins for the histogram.
    figsize : tuple, default=(12, 8)
        Figure size as (width, height) in inches.
        
    Returns:
    -------
    matplotlib.figure.Figure
        The figure containing the plots.
    """
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.stats import skew
    
    # Handle different input types for cols
    if cols is None:
        # Use all numeric columns (limit to 9 for readability)
        cols = df.select_dtypes(include='number').columns[:9]
    elif isinstance(cols, str):
        # Convert single column name to a list
        cols = [cols]
    elif not isinstance(cols, (list, pd.Index)):
        raise TypeError("'cols' must be a string, list, pandas.Index, or None")
    
    # Check if specified columns exist in the DataFrame
    missing_cols = [col for col in cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Columns not found in DataFrame: {missing_cols}")
    
    # Filter out non-numeric columns
    numeric_cols = [col for col in cols if df[col].dtype.kind in 'iufc']
    if not numeric_cols:
        raise ValueError("No numeric columns selected for plotting")
    
    # Determine subplot grid dimensions
    n_cols = min(3, len(numeric_cols))  # Max 3 columns in the grid
    n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
    
    # Create figure and subplots
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    if n_rows * n_cols == 1:  # If only one subplot, axes is not a list
        axes = np.array([axes])
    axes = axes.flatten()
    
    # Plot each column
    for i, col in enumerate(numeric_cols):
        ax = axes[i]
        
        # Calculate skewness
        skewness = skew(df[col].dropna())
        
        # Plot histogram
        df[col].hist(bins=bins, ax=ax, alpha=0.7)
        
        # Add a vertical line for the mean
        mean_val = df[col].mean()
        median_val = df[col].median()
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=1.5, label=f'Mean: {mean_val:.2f}')
        ax.axvline(median_val, color='green', linestyle='-', linewidth=1.5, label=f'Median: {median_val:.2f}')
        
        # Set title and labels
        if abs(skewness) < 0.5:
            skew_desc = "approximately symmetric"
        elif abs(skewness) < 1.0:
            skew_desc = "moderately skewed"
        else:
            skew_desc = "highly skewed"
            
        direction = "positively" if skewness > 0 else "negatively"
        if abs(skewness) >= 0.5:
            skew_text = f"{direction} {skew_desc}"
        else:
            skew_text = skew_desc
            
        ax.set_title(f'{col}\nSkew: {skewness:.4f} ({skew_text})')
        ax.set_xlabel(col)
        ax.set_ylabel('Frequency')
        ax.legend()
    
    # Hide unused subplots
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)
    
    plt.tight_layout()
    plt.show()
    
    return fig


def fill_missing(df, method=None, cols=None):
    """
    Fill missing values in a DataFrame using a specified method.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    method : str or dict
        The method to use for filling missing values.
        If a string, it should be one of 'mean', 'median', 'mode', 'ffill', 'bfill', or a constant value.
        If a dictionary, it should map column names to the method to use for that column.
    cols : str, list, or None
        Column(s) to fill missing values in.
        If None, fills missing values in all columns.

    Returns:
    -------
    pandas.DataFrame
        DataFrame with missing values filled.
    """
    result = df.copy()
    
    # Handle different input types for cols
    if cols is None:
        cols = df.columns
    elif isinstance(cols, str):
        cols = [cols]
    
    # Check if specified columns exist in the DataFrame
    missing_cols = [col for col in cols if col not in df.columns]
    if missing_cols:
        print(f"Warning: Columns {missing_cols} not found in DataFrame.")
        cols = [col for col in cols if col in df.columns]
    
    # Fill missing values based on method
    for col in cols:
        # Skip columns with no missing values
        if df[col].isna().sum() == 0:
            continue
        
        # Determine method for this column
        col_method = method[col] if isinstance(method, dict) and col in method else method
        
        # Apply method
        if col_method == "mean" and pd.api.types.is_numeric_dtype(df[col]):
            result[col] = result[col].fillna(df[col].mean())
            print(f"Column '{col}': Filled {df[col].isna().sum()} missing values with mean ({df[col].mean():.4f})")
        
        elif col_method == "median" and pd.api.types.is_numeric_dtype(df[col]):
            result[col] = result[col].fillna(df[col].median())
            print(f"Column '{col}': Filled {df[col].isna().sum()} missing values with median ({df[col].median():.4f})")
        
        elif col_method == "mode":
            mode_value = df[col].mode()[0] if not df[col].mode().empty else None
            if mode_value is not None:
                result[col] = result[col].fillna(mode_value)
                print(f"Column '{col}': Filled {df[col].isna().sum()} missing values with mode ({mode_value})")
        
        elif col_method == "ffill":
            result[col] = result[col].fillna(method='ffill')
            print(f"Column '{col}': Filled missing values with forward fill")
        
        elif col_method == "bfill":
            result[col] = result[col].fillna(method='bfill')
            print(f"Column '{col}': Filled missing values with backward fill")
        
        elif col_method is not None:
            # Use constant value
            result[col] = result[col].fillna(col_method)
            print(f"Column '{col}': Filled {df[col].isna().sum()} missing values with constant ({col_method})")
    
    # Print summary
    total_missing_before = df[cols].isna().sum().sum()
    total_missing_after = result[cols].isna().sum().sum()
    print(f"\nTotal missing values before: {total_missing_before}")
    print(f"Total missing values after: {total_missing_after}")
    print(f"Filled {total_missing_before - total_missing_after} missing values")
    
    return result


def correlation_analysis(df, method='pearson', threshold=0.0, plot=True, figsize=(12, 10)):
    """
    Analyze correlations between numeric columns in a DataFrame.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    method : {'pearson', 'kendall', 'spearman'}, default='pearson'
        Method of correlation:
        - 'pearson': Standard correlation coefficient
        - 'kendall': Kendall Tau correlation coefficient
        - 'spearman': Spearman rank correlation
    threshold : float, default=0.0
        Minimum absolute correlation value to display.
    plot : bool, default=True
        Whether to plot the correlation matrix.
    figsize : tuple, default=(12, 10)
        Figure size as (width, height) in inches.
        
    Returns:
    -------
    pandas.DataFrame
        DataFrame containing the correlation matrix.
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Select numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns
    
    if len(numeric_cols) < 2:
        print("Not enough numeric columns for correlation analysis.")
        return None
    
    # Calculate correlation matrix
    corr_matrix = df[numeric_cols].corr(method=method)
    
    # Filter by threshold
    if threshold > 0:
        corr_matrix_filtered = corr_matrix.copy()
        corr_matrix_filtered = corr_matrix_filtered.where(
            (abs(corr_matrix_filtered) >= threshold) | (corr_matrix_filtered.values == 1), 
            other=np.nan
        )
    else:
        corr_matrix_filtered = corr_matrix
    
    # Plot correlation matrix
    if plot:
        plt.figure(figsize=figsize)
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        cmap = sns.diverging_palette(230, 20, as_cmap=True)
        
        sns.heatmap(
            corr_matrix, 
            annot=True, 
            mask=mask, 
            cmap=cmap, 
            vmin=-1, 
            vmax=1, 
            center=0,
            square=True, 
            linewidths=.5, 
            cbar_kws={"shrink": .5}
        )
        
        plt.title(f'{method.capitalize()} Correlation Matrix', fontsize=16)
        plt.tight_layout()
        plt.show()
    
    # Print strongest correlations
    print(f"Strongest {method.capitalize()} Correlations:")
    corr_pairs = []
    
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            col1 = corr_matrix.columns[i]
            col2 = corr_matrix.columns[j]
            corr_value = corr_matrix.iloc[i, j]
            
            if abs(corr_value) >= threshold:
                corr_pairs.append((col1, col2, corr_value))
    
    # Sort by absolute correlation value
    corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
    
    # Print top correlations
    for col1, col2, corr_value in corr_pairs:
        correlation_type = "positive" if corr_value > 0 else "negative"
        strength = "strong" if abs(corr_value) > 0.7 else "moderate" if abs(corr_value) > 0.3 else "weak"
        print(f"- {col1} and {col2}: {corr_value:.4f} ({strength} {correlation_type} correlation)")
    
    return corr_matrix


def distribution_analysis(df, cols=None, bins=30, figsize=(15, 10)):
    """
    Analyze the distribution of numeric columns in a DataFrame.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    cols : list or None, default=None
        List of column names to analyze. If None, analyzes all numeric columns.
    bins : int, default=30
        Number of bins for histograms.
    figsize : tuple, default=(15, 10)
        Figure size as (width, height) in inches.
        
    Returns:
    -------
    dict
        Dictionary containing distribution statistics for each column.
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    from scipy import stats
    
    # Select columns to analyze
    if cols is None:
        cols = df.select_dtypes(include=['number']).columns
    else:
        # Filter out non-existent columns
        cols = [col for col in cols if col in df.columns]
        # Filter out non-numeric columns
        num_cols = df.select_dtypes(include=['number']).columns
        cols = [col for col in cols if col in num_cols]
    
    if len(cols) == 0:
        print("No valid numeric columns found for distribution analysis.")
        return {}
    
    # Determine subplot grid dimensions
    n_cols = min(3, len(cols))  # Max 3 columns in the grid
    n_rows = (len(cols) + n_cols - 1) // n_cols
    
    # Create figure and subplots
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    if n_rows * n_cols == 1:  # If only one subplot, axes is not a list
        axes = np.array([axes])
    axes = axes.flatten()
    
    # Dictionary to store distribution statistics
    dist_stats = {}
    
    # Analyze each column
    for i, col in enumerate(cols):
        # Skip columns with all missing values
        if df[col].isnull().all():
            continue
        
        # Get non-missing values
        values = df[col].dropna()
        
        # Calculate statistics
        mean_val = values.mean()
        median_val = values.median()
        mode_val = values.mode()[0] if not values.mode().empty else np.nan
        std_val = values.std()
        skewness = stats.skew(values)
        kurtosis = stats.kurtosis(values)
        
        # Store statistics
        dist_stats[col] = {
            'mean': mean_val,
            'median': median_val,
            'mode': mode_val,
            'std': std_val,
            'min': values.min(),
            'max': values.max(),
            'range': values.max() - values.min(),
            'skewness': skewness,
            'kurtosis': kurtosis,
            'q1': values.quantile(0.25),
            'q3': values.quantile(0.75),
            'iqr': values.quantile(0.75) - values.quantile(0.25)
        }
        
        # Plot histogram and KDE
        ax = axes[i]
        sns.histplot(values, bins=bins, kde=True, ax=ax)
        
        # Add vertical lines for mean and median
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=1.5, label=f'Mean: {mean_val:.2f}')
        ax.axvline(median_val, color='green', linestyle='-', linewidth=1.5, label=f'Median: {median_val:.2f}')
        
        # Set title and labels
        if abs(skewness) < 0.5:
            skew_desc = "approximately symmetric"
        elif abs(skewness) < 1.0:
            skew_desc = "moderately skewed"
        else:
            skew_desc = "highly skewed"
            
        direction = "positively" if skewness > 0 else "negatively"
        if abs(skewness) >= 0.5:
            skew_text = f"{direction} {skew_desc}"
        else:
            skew_text = skew_desc
            
        ax.set_title(f'{col}\nSkew: {skewness:.4f} ({skew_text})')
        ax.set_xlabel(col)
        ax.set_ylabel('Frequency')
        ax.legend()
    
    # Hide unused subplots
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)
    
    plt.tight_layout()
    plt.show()
    
    # Print summary statistics
    print("Distribution Statistics:")
    for col, stats in dist_stats.items():
        print(f"\n{col}:")
        for stat, value in stats.items():
            print(f"  {stat}: {value}")
    
    return dist_stats


def categorical_analysis(df, cols=None, top_n=10, figsize=(15, 10)):
    """
    Analyze categorical columns in a DataFrame.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    cols : list or None, default=None
        List of column names to analyze. If None, analyzes all object and categorical columns.
    top_n : int, default=10
        Number of top categories to display.
    figsize : tuple, default=(15, 10)
        Figure size as (width, height) in inches.
        
    Returns:
    -------
    dict
        Dictionary containing analysis results for each column.
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Select columns to analyze
    if cols is None:
        cols = df.select_dtypes(include=['object', 'category']).columns
    else:
        # Filter out non-existent columns
        cols = [col for col in cols if col in df.columns]
    
    if len(cols) == 0:
        print("No valid categorical columns found for analysis.")
        return {}
    
    # Determine subplot grid dimensions
    n_cols = min(2, len(cols))  # Max 2 columns in the grid
    n_rows = (len(cols) + n_cols - 1) // n_cols
    
    # Create figure and subplots
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    if n_rows * n_cols == 1:  # If only one subplot, axes is not a list
        axes = np.array([axes])
    axes = axes.flatten()
    
    # Dictionary to store analysis results
    results = {}
    
    # Analyze each column
    for i, col in enumerate(cols):
        # Calculate value counts
        value_counts = df[col].value_counts(dropna=False)
        
        # Store results
        results[col] = {
            'unique_values': df[col].nunique(),
            'missing_values': df[col].isna().sum(),
            'missing_percentage': df[col].isna().mean() * 100,
            'top_values': value_counts.head(top_n).to_dict()
        }
        
        # Plot bar chart
        ax = axes[i]
        top_counts = value_counts.head(top_n)
        sns.barplot(x=top_counts.index.astype(str), y=top_counts.values, ax=ax)
        
        # Add count and percentage labels
        total = len(df)
        for j, p in enumerate(ax.patches):
            height = p.get_height()
            percentage = height / total * 100
            ax.text(p.get_x() + p.get_width()/2., height + 0.1,
                   f'{int(height)}\n({percentage:.1f}%)',
                   ha="center", fontsize=9)
        
        # Set title and labels
        ax.set_title(f'Top {top_n} values for {col}')
        ax.set_xlabel(col)
        ax.set_ylabel('Count')
        
        # Rotate x-axis labels if there are many categories
        if len(top_counts) > 5:
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    
    # Hide unused subplots
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)
    
    plt.tight_layout()
    plt.show()
    
    # Print summary
    print("Categorical Analysis:")
    for col, res in results.items():
        print(f"\n{col}:")
        print(f"  Unique values: {res['unique_values']}")
        print(f"  Missing values: {res['missing_values']} ({res['missing_percentage']:.2f}%)")
        print(f"  Top {min(top_n, len(res['top_values']))} values:")
        for val, count in list(res['top_values'].items())[:top_n]:
            print(f"    - {val}: {count} ({count/len(df)*100:.2f}%)")
    
    return results
