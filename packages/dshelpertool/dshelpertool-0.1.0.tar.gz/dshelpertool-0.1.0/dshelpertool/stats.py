"""
Statistics module for statistical analysis and hypothesis testing.
"""
import pandas as pd
import numpy as np


def describe_all(df, include='all', percentiles=None):
    """
    Enhanced describe function that works for all column types.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    include : list-like, default='all'
        A list of dtypes or 'all' to include in the result.
    percentiles : list-like, default=None
        The percentiles to include in the output. Default is [0.25, 0.5, 0.75].
        
    Returns:
    -------
    pandas.DataFrame
        DataFrame containing descriptive statistics.
    """
    # Get basic describe
    desc = df.describe(include=include, percentiles=percentiles)
    
    # Add additional statistics for numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        # Add skewness and kurtosis
        from scipy.stats import skew, kurtosis
        
        skewness = df[numeric_cols].apply(lambda x: skew(x.dropna()))
        kurt = df[numeric_cols].apply(lambda x: kurtosis(x.dropna()))
        
        # Add to describe DataFrame
        desc.loc['skew'] = skewness
        desc.loc['kurtosis'] = kurt
        
        # Add missing values count and percentage
        missing = df[numeric_cols].isnull().sum()
        missing_pct = df[numeric_cols].isnull().mean() * 100
        
        desc.loc['missing'] = missing
        desc.loc['missing_pct'] = missing_pct
    
    # Add additional statistics for object/categorical columns
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    if len(cat_cols) > 0 and include in ['all', 'object', 'category'] or any(col in include for col in cat_cols):
        # Add missing values count and percentage
        missing = df[cat_cols].isnull().sum()
        missing_pct = df[cat_cols].isnull().mean() * 100
        
        # Add to describe DataFrame if columns exist
        for col in cat_cols:
            if col in desc.columns:
                desc.loc['missing', col] = missing[col]
                desc.loc['missing_pct', col] = missing_pct[col]
    
    # Print the enhanced describe
    print("Enhanced Descriptive Statistics:")
    print(desc)
    
    return desc


def group_stats(df, group_by, agg_cols=None, agg_funcs=None):
    """
    Calculate statistics for groups in a DataFrame.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    group_by : str or list
        Column name or list of column names to group by.
    agg_cols : list or None, default=None
        List of column names to aggregate. If None, uses all numeric columns.
    agg_funcs : list, dict, or None, default=None
        Aggregation functions to apply. If None, uses ['count', 'mean', 'std', 'min', 'max'].
        
    Returns:
    -------
    pandas.DataFrame
        DataFrame containing group statistics.
    """
    # Handle input parameters
    if isinstance(group_by, str):
        group_by = [group_by]
    
    # Check if group_by columns exist
    missing_cols = [col for col in group_by if col not in df.columns]
    if missing_cols:
        print(f"Warning: Columns {missing_cols} not found in DataFrame.")
        group_by = [col for col in group_by if col in df.columns]
        if not group_by:
            print("No valid columns to group by.")
            return None
    
    # Select columns to aggregate
    if agg_cols is None:
        agg_cols = df.select_dtypes(include=['number']).columns
        # Remove group_by columns from agg_cols
        agg_cols = [col for col in agg_cols if col not in group_by]
    elif isinstance(agg_cols, str):
        agg_cols = [agg_cols]
    
    # Check if agg_cols exist
    missing_cols = [col for col in agg_cols if col not in df.columns]
    if missing_cols:
        print(f"Warning: Columns {missing_cols} not found in DataFrame.")
        agg_cols = [col for col in agg_cols if col in df.columns]
        if not agg_cols:
            print("No valid columns to aggregate.")
            return None
    
    # Set default aggregation functions
    if agg_funcs is None:
        agg_funcs = ['count', 'mean', 'std', 'min', 'max']
    
    # Create aggregation dictionary if needed
    if not isinstance(agg_funcs, dict):
        agg_dict = {col: agg_funcs for col in agg_cols}
    else:
        agg_dict = agg_funcs
    
    # Perform groupby and aggregation
    grouped = df.groupby(group_by).agg(agg_dict)
    
    # Print summary
    print(f"Group Statistics (grouped by {', '.join(group_by)}):")
    print(grouped)
    
    return grouped


def outlier_detection(df, cols=None, method='iqr', threshold=1.5):
    """
    Detect outliers in numeric columns using different methods.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    cols : list or None, default=None
        List of column names to check for outliers. If None, checks all numeric columns.
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
        Dictionary with column names as keys and boolean masks of outliers as values.
    """
    from scipy import stats
    
    # Select columns to analyze
    if cols is None:
        cols = df.select_dtypes(include=['number']).columns
    elif isinstance(cols, str):
        cols = [cols]
    
    # Check if columns exist
    missing_cols = [col for col in cols if col not in df.columns]
    if missing_cols:
        print(f"Warning: Columns {missing_cols} not found in DataFrame.")
        cols = [col for col in cols if col in df.columns]
    
    # Filter out non-numeric columns
    num_cols = df.select_dtypes(include=['number']).columns
    cols = [col for col in cols if col in num_cols]
    
    if len(cols) == 0:
        print("No valid numeric columns found for outlier detection.")
        return {}
    
    # Dictionary to store outlier masks
    outlier_masks = {}
    outlier_counts = {}
    
    # Detect outliers for each column
    for col in cols:
        # Skip columns with all missing values
        if df[col].isnull().all():
            continue
        
        # Get non-missing values
        values = df[col].dropna()
        
        # Detect outliers based on the selected method
        if method == 'iqr':
            Q1 = values.quantile(0.25)
            Q3 = values.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            
            outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
            outlier_masks[col] = outlier_mask
            
            outlier_counts[col] = {
                'method': 'IQR',
                'threshold': threshold,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'outlier_count': outlier_mask.sum(),
                'outlier_percentage': outlier_mask.mean() * 100
            }
            
        elif method == 'zscore':
            z_scores = stats.zscore(values)
            z_score_dict = dict(zip(values.index, z_scores))
            
            # Create a Series of z-scores with the same index as the original DataFrame
            z_score_series = pd.Series([z_score_dict.get(i, np.nan) for i in df.index], index=df.index)
            
            # Identify outliers
            outlier_mask = (abs(z_score_series) > threshold) & ~df[col].isnull()
            outlier_masks[col] = outlier_mask
            
            outlier_counts[col] = {
                'method': 'Z-score',
                'threshold': threshold,
                'outlier_count': outlier_mask.sum(),
                'outlier_percentage': outlier_mask.mean() * 100
            }
            
        elif method == 'std':
            mean = values.mean()
            std = values.std()
            lower_bound = mean - threshold * std
            upper_bound = mean + threshold * std
            
            outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
            outlier_masks[col] = outlier_mask
            
            outlier_counts[col] = {
                'method': 'Standard Deviation',
                'threshold': threshold,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'outlier_count': outlier_mask.sum(),
                'outlier_percentage': outlier_mask.mean() * 100
            }
            
        else:
            print(f"Invalid method: {method}. Using 'iqr' instead.")
            Q1 = values.quantile(0.25)
            Q3 = values.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            
            outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
            outlier_masks[col] = outlier_mask
            
            outlier_counts[col] = {
                'method': 'IQR',
                'threshold': threshold,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'outlier_count': outlier_mask.sum(),
                'outlier_percentage': outlier_mask.mean() * 100
            }
    
    # Print summary
    print(f"Outlier Detection Summary (method: {method}, threshold: {threshold}):")
    for col, info in outlier_counts.items():
        print(f"\n{col}:")
        for key, value in info.items():
            print(f"  {key}: {value}")
    
    return outlier_masks, outlier_counts


def hypothesis_test(df, group_col, value_col, test_type='ttest', alpha=0.05):
    """
    Perform hypothesis tests to compare groups.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    group_col : str
        Column name containing group labels.
    value_col : str
        Column name containing values to compare.
    test_type : str, default='ttest'
        Type of test to perform:
        - 'ttest': Independent t-test (for 2 groups)
        - 'anova': One-way ANOVA (for 3+ groups)
        - 'mannwhitney': Mann-Whitney U test (for 2 groups, non-parametric)
        - 'kruskal': Kruskal-Wallis H test (for 3+ groups, non-parametric)
    alpha : float, default=0.05
        Significance level.
        
    Returns:
    -------
    dict
        Dictionary containing test results.
    """
    from scipy import stats
    
    # Check if columns exist
    if group_col not in df.columns:
        print(f"Error: Group column '{group_col}' not found in DataFrame.")
        return None
    
    if value_col not in df.columns:
        print(f"Error: Value column '{value_col}' not found in DataFrame.")
        return None
    
    # Check if value column is numeric
    if not pd.api.types.is_numeric_dtype(df[value_col]):
        print(f"Error: Value column '{value_col}' must be numeric.")
        return None
    
    # Get unique groups
    groups = df[group_col].dropna().unique()
    
    if len(groups) < 2:
        print(f"Error: Need at least 2 groups for comparison. Found {len(groups)} groups.")
        return None
    
    # Prepare data for test
    data_by_group = [df[df[group_col] == group][value_col].dropna() for group in groups]
    
    # Perform the appropriate test
    if test_type == 'ttest':
        if len(groups) != 2:
            print(f"Warning: t-test requires exactly 2 groups. Found {len(groups)} groups. Using first 2 groups.")
            data_by_group = data_by_group[:2]
            groups = groups[:2]
        
        stat, p_value = stats.ttest_ind(data_by_group[0], data_by_group[1], equal_var=False)
        test_name = "Independent t-test"
        
    elif test_type == 'anova':
        if len(groups) < 3:
            print(f"Warning: ANOVA is typically used for 3+ groups. Found {len(groups)} groups.")
        
        stat, p_value = stats.f_oneway(*data_by_group)
        test_name = "One-way ANOVA"
        
    elif test_type == 'mannwhitney':
        if len(groups) != 2:
            print(f"Warning: Mann-Whitney U test requires exactly 2 groups. Found {len(groups)} groups. Using first 2 groups.")
            data_by_group = data_by_group[:2]
            groups = groups[:2]
        
        stat, p_value = stats.mannwhitneyu(data_by_group[0], data_by_group[1])
        test_name = "Mann-Whitney U test"
        
    elif test_type == 'kruskal':
        if len(groups) < 3:
            print(f"Warning: Kruskal-Wallis H test is typically used for 3+ groups. Found {len(groups)} groups.")
        
        stat, p_value = stats.kruskal(*data_by_group)
        test_name = "Kruskal-Wallis H test"
        
    else:
        print(f"Invalid test type: {test_type}. Using t-test instead.")
        if len(groups) != 2:
            print(f"Warning: t-test requires exactly 2 groups. Found {len(groups)} groups. Using first 2 groups.")
            data_by_group = data_by_group[:2]
            groups = groups[:2]
        
        stat, p_value = stats.ttest_ind(data_by_group[0], data_by_group[1], equal_var=False)
        test_name = "Independent t-test"
    
    # Interpret results
    if p_value < alpha:
        conclusion = f"Reject the null hypothesis (p={p_value:.4f} < {alpha})"
        interpretation = "There is a statistically significant difference between groups."
    else:
        conclusion = f"Fail to reject the null hypothesis (p={p_value:.4f} >= {alpha})"
        interpretation = "There is no statistically significant difference between groups."
    
    # Calculate group statistics
    group_stats = {}
    for i, group in enumerate(groups):
        group_stats[group] = {
            'count': len(data_by_group[i]),
            'mean': data_by_group[i].mean(),
            'std': data_by_group[i].std(),
            'min': data_by_group[i].min(),
            'max': data_by_group[i].max()
        }
    
    # Prepare results
    results = {
        'test_name': test_name,
        'groups': list(groups),
        'statistic': stat,
        'p_value': p_value,
        'alpha': alpha,
        'conclusion': conclusion,
        'interpretation': interpretation,
        'group_stats': group_stats
    }
    
    # Print results
    print(f"Hypothesis Test: {test_name}")
    print(f"Comparing '{value_col}' across groups in '{group_col}'")
    print("\nGroup Statistics:")
    for group, stats in group_stats.items():
        print(f"  {group}: n={stats['count']}, mean={stats['mean']:.4f}, std={stats['std']:.4f}")
    
    print(f"\nTest Statistic: {stat:.4f}")
    print(f"P-value: {p_value:.4f}")
    print(f"Alpha: {alpha}")
    print(f"\nConclusion: {conclusion}")
    print(f"Interpretation: {interpretation}")
    
    return results


def correlation_matrix(df, method='pearson', min_corr=0.0, plot=True, figsize=(12, 10)):
    """
    Calculate and visualize the correlation matrix for numeric columns.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    method : {'pearson', 'kendall', 'spearman'}, default='pearson'
        Method of correlation:
        - 'pearson': Standard correlation coefficient
        - 'kendall': Kendall Tau correlation coefficient
        - 'spearman': Spearman rank correlation
    min_corr : float, default=0.0
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
    
    # Filter by minimum correlation
    if min_corr > 0:
        corr_matrix_filtered = corr_matrix.copy()
        corr_matrix_filtered = corr_matrix_filtered.where(
            (abs(corr_matrix_filtered) >= min_corr) | (corr_matrix_filtered.values == 1), 
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
    
    # Extract and print strongest correlations
    corr_pairs = []
    
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            col1 = corr_matrix.columns[i]
            col2 = corr_matrix.columns[j]
            corr_value = corr_matrix.iloc[i, j]
            
            if abs(corr_value) >= min_corr:
                corr_pairs.append((col1, col2, corr_value))
    
    # Sort by absolute correlation value
    corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
    
    # Print top correlations
    print(f"Strongest {method.capitalize()} Correlations:")
    for col1, col2, corr_value in corr_pairs:
        correlation_type = "positive" if corr_value > 0 else "negative"
        strength = "strong" if abs(corr_value) > 0.7 else "moderate" if abs(corr_value) > 0.3 else "weak"
        print(f"- {col1} and {col2}: {corr_value:.4f} ({strength} {correlation_type} correlation)")
    
    return corr_matrix
