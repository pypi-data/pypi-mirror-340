"""
Basic usage examples for the dshelpertool package.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Import dshelpertool modules
from dshelpertool import overview, cleaning, dtypes, eda, stats, viz

# Create a sample DataFrame
def create_sample_data(rows=1000):
    """Create a sample DataFrame for demonstration."""
    np.random.seed(42)

    # Create a date range
    dates = pd.date_range('2021-01-01', periods=rows)

    # Create numeric columns with different distributions
    normal = np.random.normal(loc=50, scale=10, size=rows)
    skewed = np.random.exponential(scale=10, size=rows)
    uniform = np.random.uniform(low=0, high=100, size=rows)

    # Create categorical columns
    categories = ['A', 'B', 'C', 'D', 'E']
    cat1 = np.random.choice(categories, size=rows, p=[0.4, 0.3, 0.15, 0.1, 0.05])
    cat2 = np.random.choice(categories, size=rows)

    # Create a boolean column
    boolean = np.random.choice([True, False], size=rows)

    # Create a DataFrame
    df = pd.DataFrame({
        'date': dates,
        'normal': normal,
        'skewed': skewed,
        'uniform': uniform,
        'category1': cat1,
        'category2': cat2,
        'boolean': boolean
    })

    # Add some missing values
    for col in df.columns:
        mask = np.random.random(size=rows) < 0.05  # 5% missing values
        df.loc[mask, col] = np.nan

    return df

# Create a sample DataFrame
df = create_sample_data()

# Example 1: Get a quick overview of the DataFrame
print("\n=== Example 1: Quick Overview ===")
summary = overview.quick_look(df, name="Sample Data")

# Example 2: Clean column names
print("\n=== Example 2: Clean Column Names ===")
df_clean = cleaning.update_col(df, standardize_col=True)
print("Original columns:", df.columns.tolist())
print("Cleaned columns:", df_clean.columns.tolist())

# Example 3: Convert data types
print("\n=== Example 3: Convert Data Types ===")
df_typed = dtypes.to_datetime_cols(df_clean, cols="date")
print("Date column type:", df_typed["date"].dtype)

# Example 4: Check for skewness
print("\n=== Example 4: Check for Skewness ===")
eda.check_skew(df_clean, cols=["normal", "skewed", "uniform"])

# Example 5: Analyze correlations
print("\n=== Example 5: Correlation Analysis ===")
numeric_cols = ["normal", "skewed", "uniform"]
corr_matrix = stats.correlation_matrix(df_clean, method="pearson", min_corr=0.1, plot=False)
print("Correlation matrix:")
print(corr_matrix)

# Example 6: Visualize distributions
print("\n=== Example 6: Visualize Distributions ===")
print("Plotting distributions (close the plot window to continue)...")
viz.plot_distributions(df_clean, cols=numeric_cols)

# Example 7: Visualize categorical data
print("\n=== Example 7: Visualize Categorical Data ===")
print("Plotting categorical data (close the plot window to continue)...")
viz.plot_categorical(df_clean, cols=["category1", "category2"])

# Example 8: Find and handle outliers
print("\n=== Example 8: Find and Handle Outliers ===")
outliers, outlier_counts = stats.outlier_detection(df_clean, cols=numeric_cols, method="iqr")
print("Outlier counts:")
for col, info in outlier_counts.items():
    print(f"- {col}: {info['outlier_count']} outliers ({info['outlier_percentage']:.2f}%)")

# Example 9: Fill missing values
print("\n=== Example 9: Fill Missing Values ===")
missing_before = df_clean.isnull().sum().sum()
df_filled = eda.fill_missing(df_clean, method="mean", cols=numeric_cols)
missing_after = df_filled.isnull().sum().sum()
print(f"Missing values before: {missing_before}")
print(f"Missing values after: {missing_after}")
print(f"Filled {missing_before - missing_after} missing values")

# Example 10: Get value counts for categorical columns
print("\n=== Example 10: Value Counts for Categorical Columns ===")
value_counts = overview.value_counts_all(df_clean, top_n=3)

print("\nAll examples completed successfully!")
