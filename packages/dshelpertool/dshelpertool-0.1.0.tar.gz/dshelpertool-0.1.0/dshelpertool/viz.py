"""
Visualization module for creating plots and charts.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def plot_missing(df, figsize=(10, 6), plot_type='bar'):
    """
    Visualize missing values in a DataFrame.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    figsize : tuple, default=(10, 6)
        Figure size as (width, height) in inches.
    plot_type : str, default='bar'
        Type of plot to create:
        - 'bar': Bar chart of missing values by column
        - 'heatmap': Heatmap of missing values
        - 'matrix': Matrix of missing values
        
    Returns:
    -------
    matplotlib.figure.Figure
        The figure containing the plot.
    """
    # Calculate missing values
    missing = df.isnull().sum()
    missing_percent = missing / len(df) * 100
    
    # Create a DataFrame for plotting
    missing_df = pd.DataFrame({
        'Count': missing,
        'Percent': missing_percent
    }).sort_values('Count', ascending=False)
    
    # Create the appropriate plot
    if plot_type == 'bar':
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot missing counts
        bars = ax.bar(missing_df.index, missing_df['Count'], color='skyblue')
        
        # Add count and percentage labels
        for i, bar in enumerate(bars):
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                       f'{int(height)}\n({missing_df["Percent"].iloc[i]:.1f}%)',
                       ha="center", fontsize=9)
        
        # Set title and labels
        ax.set_title('Missing Values by Column', fontsize=14)
        ax.set_xlabel('Column', fontsize=12)
        ax.set_ylabel('Count', fontsize=12)
        
        # Rotate x-axis labels if there are many columns
        if len(missing_df) > 5:
            plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        
    elif plot_type == 'heatmap':
        # Create a heatmap of missing values
        plt.figure(figsize=figsize)
        sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
        plt.title('Missing Values Heatmap', fontsize=14)
        plt.tight_layout()
        
    elif plot_type == 'matrix':
        # Create a matrix of missing values
        import missingno as msno
        fig = msno.matrix(df, figsize=figsize)
        plt.title('Missing Values Matrix', fontsize=14)
        
    else:
        print(f"Invalid plot type: {plot_type}. Using 'bar' instead.")
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot missing counts
        bars = ax.bar(missing_df.index, missing_df['Count'], color='skyblue')
        
        # Add count and percentage labels
        for i, bar in enumerate(bars):
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                       f'{int(height)}\n({missing_df["Percent"].iloc[i]:.1f}%)',
                       ha="center", fontsize=9)
        
        # Set title and labels
        ax.set_title('Missing Values by Column', fontsize=14)
        ax.set_xlabel('Column', fontsize=12)
        ax.set_ylabel('Count', fontsize=12)
        
        # Rotate x-axis labels if there are many columns
        if len(missing_df) > 5:
            plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
    
    # Print summary
    print("Missing Values Summary:")
    for col, count in missing.items():
        if count > 0:
            print(f"- {col}: {count} missing values ({missing_percent[col]:.2f}%)")
    
    plt.show()
    
    return fig


def plot_distributions(df, cols=None, bins=30, figsize=(15, 10)):
    """
    Plot distributions of numeric columns.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    cols : list or None, default=None
        List of column names to plot. If None, plots all numeric columns.
    bins : int, default=30
        Number of bins for histograms.
    figsize : tuple, default=(15, 10)
        Figure size as (width, height) in inches.
        
    Returns:
    -------
    matplotlib.figure.Figure
        The figure containing the plots.
    """
    # Select columns to plot
    if cols is None:
        cols = df.select_dtypes(include=['number']).columns
    else:
        # Filter out non-existent columns
        cols = [col for col in cols if col in df.columns]
        # Filter out non-numeric columns
        num_cols = df.select_dtypes(include=['number']).columns
        cols = [col for col in cols if col in num_cols]
    
    if len(cols) == 0:
        print("No valid numeric columns found for plotting.")
        return None
    
    # Determine subplot grid dimensions
    n_cols = min(3, len(cols))  # Max 3 columns in the grid
    n_rows = (len(cols) + n_cols - 1) // n_cols
    
    # Create figure and subplots
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    if n_rows * n_cols == 1:  # If only one subplot, axes is not a list
        axes = np.array([axes])
    axes = axes.flatten()
    
    # Plot each column
    for i, col in enumerate(cols):
        ax = axes[i]
        
        # Plot histogram with KDE
        sns.histplot(df[col].dropna(), bins=bins, kde=True, ax=ax)
        
        # Add vertical lines for mean and median
        mean_val = df[col].mean()
        median_val = df[col].median()
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=1.5, label=f'Mean: {mean_val:.2f}')
        ax.axvline(median_val, color='green', linestyle='-', linewidth=1.5, label=f'Median: {median_val:.2f}')
        
        # Set title and labels
        ax.set_title(col)
        ax.set_xlabel(col)
        ax.set_ylabel('Frequency')
        ax.legend()
    
    # Hide unused subplots
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)
    
    plt.tight_layout()
    plt.show()
    
    return fig


def plot_categorical(df, cols=None, top_n=10, figsize=(15, 10)):
    """
    Plot bar charts for categorical columns.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    cols : list or None, default=None
        List of column names to plot. If None, plots all object and categorical columns.
    top_n : int, default=10
        Number of top categories to display.
    figsize : tuple, default=(15, 10)
        Figure size as (width, height) in inches.
        
    Returns:
    -------
    matplotlib.figure.Figure
        The figure containing the plots.
    """
    # Select columns to plot
    if cols is None:
        cols = df.select_dtypes(include=['object', 'category']).columns
    else:
        # Filter out non-existent columns
        cols = [col for col in cols if col in df.columns]
    
    if len(cols) == 0:
        print("No valid categorical columns found for plotting.")
        return None
    
    # Determine subplot grid dimensions
    n_cols = min(2, len(cols))  # Max 2 columns in the grid
    n_rows = (len(cols) + n_cols - 1) // n_cols
    
    # Create figure and subplots
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    if n_rows * n_cols == 1:  # If only one subplot, axes is not a list
        axes = np.array([axes])
    axes = axes.flatten()
    
    # Plot each column
    for i, col in enumerate(cols):
        ax = axes[i]
        
        # Calculate value counts
        value_counts = df[col].value_counts(dropna=False)
        
        # Get top N categories
        top_counts = value_counts.head(top_n)
        
        # Plot bar chart
        bars = ax.bar(top_counts.index.astype(str), top_counts.values, color='skyblue')
        
        # Add count and percentage labels
        total = len(df)
        for j, bar in enumerate(bars):
            height = bar.get_height()
            percentage = height / total * 100
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
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
    
    return fig


def plot_correlation(df, method='pearson', figsize=(12, 10), annot=True, cmap='coolwarm'):
    """
    Plot correlation matrix for numeric columns.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    method : {'pearson', 'kendall', 'spearman'}, default='pearson'
        Method of correlation:
        - 'pearson': Standard correlation coefficient
        - 'kendall': Kendall Tau correlation coefficient
        - 'spearman': Spearman rank correlation
    figsize : tuple, default=(12, 10)
        Figure size as (width, height) in inches.
    annot : bool, default=True
        Whether to annotate the heatmap with correlation values.
    cmap : str or colormap, default='coolwarm'
        Colormap to use for the heatmap.
        
    Returns:
    -------
    matplotlib.figure.Figure
        The figure containing the plot.
    """
    # Select numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns
    
    if len(numeric_cols) < 2:
        print("Not enough numeric columns for correlation analysis.")
        return None
    
    # Calculate correlation matrix
    corr_matrix = df[numeric_cols].corr(method=method)
    
    # Plot correlation matrix
    plt.figure(figsize=figsize)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    
    sns.heatmap(
        corr_matrix, 
        annot=annot, 
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
            
            corr_pairs.append((col1, col2, corr_value))
    
    # Sort by absolute correlation value
    corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
    
    # Print top correlations
    print(f"Strongest {method.capitalize()} Correlations:")
    for col1, col2, corr_value in corr_pairs[:10]:  # Print top 10
        correlation_type = "positive" if corr_value > 0 else "negative"
        strength = "strong" if abs(corr_value) > 0.7 else "moderate" if abs(corr_value) > 0.3 else "weak"
        print(f"- {col1} and {col2}: {corr_value:.4f} ({strength} {correlation_type} correlation)")
    
    return plt.gcf()


def plot_boxplots(df, cols=None, figsize=(15, 10)):
    """
    Plot boxplots for numeric columns.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    cols : list or None, default=None
        List of column names to plot. If None, plots all numeric columns.
    figsize : tuple, default=(15, 10)
        Figure size as (width, height) in inches.
        
    Returns:
    -------
    matplotlib.figure.Figure
        The figure containing the plots.
    """
    # Select columns to plot
    if cols is None:
        cols = df.select_dtypes(include=['number']).columns
    else:
        # Filter out non-existent columns
        cols = [col for col in cols if col in df.columns]
        # Filter out non-numeric columns
        num_cols = df.select_dtypes(include=['number']).columns
        cols = [col for col in cols if col in num_cols]
    
    if len(cols) == 0:
        print("No valid numeric columns found for plotting.")
        return None
    
    # Determine subplot grid dimensions
    n_cols = min(3, len(cols))  # Max 3 columns in the grid
    n_rows = (len(cols) + n_cols - 1) // n_cols
    
    # Create figure and subplots
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    if n_rows * n_cols == 1:  # If only one subplot, axes is not a list
        axes = np.array([axes])
    axes = axes.flatten()
    
    # Plot each column
    for i, col in enumerate(cols):
        ax = axes[i]
        
        # Plot boxplot
        sns.boxplot(y=df[col].dropna(), ax=ax)
        
        # Add swarmplot for data points
        sns.swarmplot(y=df[col].dropna(), ax=ax, color='black', alpha=0.5, size=3)
        
        # Set title and labels
        ax.set_title(col)
        ax.set_ylabel(col)
    
    # Hide unused subplots
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)
    
    plt.tight_layout()
    plt.show()
    
    return fig


def plot_scatter_matrix(df, cols=None, figsize=(15, 15)):
    """
    Plot scatter matrix for numeric columns.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    cols : list or None, default=None
        List of column names to plot. If None, plots all numeric columns (up to 5).
    figsize : tuple, default=(15, 15)
        Figure size as (width, height) in inches.
        
    Returns:
    -------
    matplotlib.figure.Figure
        The figure containing the plots.
    """
    # Select columns to plot
    if cols is None:
        cols = df.select_dtypes(include=['number']).columns[:5]  # Limit to 5 columns for readability
    else:
        # Filter out non-existent columns
        cols = [col for col in cols if col in df.columns]
        # Filter out non-numeric columns
        num_cols = df.select_dtypes(include=['number']).columns
        cols = [col for col in cols if col in num_cols]
    
    if len(cols) < 2:
        print("Need at least 2 numeric columns for scatter matrix.")
        return None
    
    # Create scatter matrix
    fig = sns.pairplot(df[cols], diag_kind='kde', plot_kws={'alpha': 0.6})
    plt.suptitle('Scatter Matrix', y=1.02, fontsize=16)
    plt.tight_layout()
    plt.show()
    
    return fig


def plot_time_series(df, date_col, value_cols, freq=None, figsize=(15, 8)):
    """
    Plot time series data.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    date_col : str
        Column name containing dates.
    value_cols : str or list
        Column name or list of column names containing values to plot.
    freq : str or None, default=None
        Frequency to resample the data (e.g., 'D', 'W', 'M', 'Q', 'Y').
    figsize : tuple, default=(15, 8)
        Figure size as (width, height) in inches.
        
    Returns:
    -------
    matplotlib.figure.Figure
        The figure containing the plot.
    """
    # Check if date column exists
    if date_col not in df.columns:
        print(f"Error: Date column '{date_col}' not found in DataFrame.")
        return None
    
    # Convert date column to datetime if needed
    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        try:
            df = df.copy()
            df[date_col] = pd.to_datetime(df[date_col])
        except:
            print(f"Error: Could not convert '{date_col}' to datetime.")
            return None
    
    # Handle value columns
    if isinstance(value_cols, str):
        value_cols = [value_cols]
    
    # Check if value columns exist
    missing_cols = [col for col in value_cols if col not in df.columns]
    if missing_cols:
        print(f"Error: Value columns {missing_cols} not found in DataFrame.")
        value_cols = [col for col in value_cols if col in df.columns]
        if not value_cols:
            return None
    
    # Set date column as index
    df_plot = df.copy()
    df_plot.set_index(date_col, inplace=True)
    
    # Resample data if frequency is specified
    if freq is not None:
        df_plot = df_plot[value_cols].resample(freq).mean()
    
    # Plot time series
    fig, ax = plt.subplots(figsize=figsize)
    
    for col in value_cols:
        ax.plot(df_plot.index, df_plot[col], label=col)
    
    # Set title and labels
    ax.set_title('Time Series Plot', fontsize=14)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Value', fontsize=12)
    
    # Add legend
    ax.legend()
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Format x-axis dates
    fig.autofmt_xdate()
    
    plt.tight_layout()
    plt.show()
    
    return fig


def plot_group_comparison(df, group_col, value_col, plot_type='box', figsize=(12, 8)):
    """
    Plot comparison of a value column across different groups.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    group_col : str
        Column name containing group labels.
    value_col : str
        Column name containing values to compare.
    plot_type : str, default='box'
        Type of plot to create:
        - 'box': Boxplot
        - 'violin': Violin plot
        - 'bar': Bar chart of means
        - 'strip': Strip plot
    figsize : tuple, default=(12, 8)
        Figure size as (width, height) in inches.
        
    Returns:
    -------
    matplotlib.figure.Figure
        The figure containing the plot.
    """
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
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Create the appropriate plot
    if plot_type == 'box':
        sns.boxplot(x=group_col, y=value_col, data=df, ax=ax)
        sns.stripplot(x=group_col, y=value_col, data=df, color='black', alpha=0.5, size=3, ax=ax)
        
    elif plot_type == 'violin':
        sns.violinplot(x=group_col, y=value_col, data=df, ax=ax)
        sns.stripplot(x=group_col, y=value_col, data=df, color='black', alpha=0.5, size=3, ax=ax)
        
    elif plot_type == 'bar':
        # Calculate means and standard errors
        grouped = df.groupby(group_col)[value_col].agg(['mean', 'sem'])
        
        # Plot bar chart
        bars = ax.bar(grouped.index, grouped['mean'], yerr=grouped['sem'], capsize=5, color='skyblue')
        
        # Add mean labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                   f'{height:.2f}', ha="center", fontsize=9)
        
    elif plot_type == 'strip':
        sns.stripplot(x=group_col, y=value_col, data=df, ax=ax, jitter=True, alpha=0.7)
        
    else:
        print(f"Invalid plot type: {plot_type}. Using 'box' instead.")
        sns.boxplot(x=group_col, y=value_col, data=df, ax=ax)
        sns.stripplot(x=group_col, y=value_col, data=df, color='black', alpha=0.5, size=3, ax=ax)
    
    # Set title and labels
    ax.set_title(f'Comparison of {value_col} by {group_col}', fontsize=14)
    ax.set_xlabel(group_col, fontsize=12)
    ax.set_ylabel(value_col, fontsize=12)
    
    # Rotate x-axis labels if there are many groups
    if len(df[group_col].unique()) > 5:
        plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.show()
    
    return fig
