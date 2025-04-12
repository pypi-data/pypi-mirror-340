"""
Data cleaning examples for the dshelpertool package.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Import dshelpertool modules
from dshelpertool import cleaning, dtypes, eda

# Load a messy dataset
def create_messy_data(rows=1000):
    """Create a messy DataFrame for demonstration."""
    np.random.seed(42)

    # Create a date range with some invalid dates
    dates = []
    for i in range(rows):
        if i % 20 == 0:  # 5% invalid dates
            dates.append("invalid date")
        elif i % 25 == 0:  # 4% empty dates
            dates.append(None)
        else:
            dates.append(pd.Timestamp('2021-01-01') + pd.Timedelta(days=i))

    # Create numeric columns with some invalid values
    numeric1 = []
    numeric2 = []
    for i in range(rows):
        if i % 15 == 0:  # ~7% invalid values
            numeric1.append("NaN")
            numeric2.append("invalid")
        elif i % 18 == 0:  # ~6% missing values
            numeric1.append(None)
            numeric2.append(None)
        else:
            numeric1.append(np.random.normal(loc=50, scale=10))
            numeric2.append(np.random.exponential(scale=10))

    # Create categorical columns with inconsistent values
    categories = ['Category A', 'Category B', 'Category C', 'category a', 'category b', 'CATEGORY C']
    cat1 = np.random.choice(categories, size=rows)

    # Create a column with mixed types
    mixed = []
    for i in range(rows):
        if i % 3 == 0:
            mixed.append(i)
        elif i % 3 == 1:
            mixed.append(f"String {i}")
        else:
            mixed.append(f"{i}.{i}")

    # Create a column with extra spaces and special characters
    text = []
    for i in range(rows):
        if i % 4 == 0:
            text.append(f"  Text with spaces  {i}  ")
        elif i % 4 == 1:
            text.append(f"Text-with-hyphens-{i}")
        elif i % 4 == 2:
            text.append(f"Text_with_underscores_{i}")
        else:
            text.append(f"Text with special chars: {i}!")

    # Create a DataFrame with messy column names
    df = pd.DataFrame({
        ' Date Column ': dates,
        'Numeric Column 1': numeric1,
        'Numeric-Column-2': numeric2,
        'Categorical_Column': cat1,
        'Mixed Types': mixed,
        'TEXT WITH SPACES': text
    })

    return df

# Create a messy DataFrame
df_messy = create_messy_data()

print("=== Original Messy DataFrame ===")
print(df_messy.head())
print("\nData Types:")
print(df_messy.dtypes)
print("\nMissing Values:")
print(df_messy.isnull().sum())

# Step 1: Standardize column names
print("\n=== Step 1: Standardize Column Names ===")
df_clean = cleaning.update_col(df_messy, standardize_col=True)
print("Standardized columns:", df_clean.columns.tolist())

# Step 2: Convert data types
print("\n=== Step 2: Convert Data Types ===")
# Convert date column
df_clean = dtypes.to_datetime_cols(df_clean, cols="date_column")
print("Date column type:", df_clean["date_column"].dtype)

# Convert numeric columns
df_clean = dtypes.to_numeric_cols(df_clean, ["numeric_column_1", "numeric_column_2"])
print("Numeric column types:")
print(df_clean[["numeric_column_1", "numeric_column_2"]].dtypes)

# Convert categorical column
df_clean = dtypes.to_category_cols(df_clean, cols="categorical_column")
print("Categorical column type:", df_clean["categorical_column"].dtype)

# Step 3: Clean text data
print("\n=== Step 3: Clean Text Data ===")
df_clean = cleaning.clean_text(df_clean, columns=["text_with_spaces"],
                              lower=True, strip=True, remove_special=True)
print("Cleaned text sample:")
print(df_clean["text_with_spaces"].head())

# Step 4: Standardize categorical values
print("\n=== Step 4: Standardize Categorical Values ===")
# Create a mapping for standardizing categories
category_mapping = {
    'Category A': 'category_a',
    'Category B': 'category_b',
    'Category C': 'category_c',
    'category a': 'category_a',
    'category b': 'category_b',
    'CATEGORY C': 'category_c'
}
df_clean = cleaning.replace_values(df_clean, columns=["categorical_column"],
                                  to_replace=category_mapping)
print("Standardized categories:")
print(df_clean["categorical_column"].value_counts())

# Step 5: Handle missing values
print("\n=== Step 5: Handle Missing Values ===")
# Count missing values before
missing_before = df_clean.isnull().sum().sum()
print(f"Missing values before: {missing_before}")

# Fill missing values in numeric columns with mean
df_clean = eda.fill_missing(df_clean, method="mean",
                           cols=["numeric_column_1", "numeric_column_2"])

# Fill missing values in date column with forward fill
df_clean = eda.fill_missing(df_clean, method="ffill", cols=["date_column"])

# Count missing values after
missing_after = df_clean.isnull().sum().sum()
print(f"Missing values after: {missing_after}")
print(f"Filled {missing_before - missing_after} missing values")

# Step 6: Remove duplicates
print("\n=== Step 6: Remove Duplicates ===")
# Add some duplicate rows for demonstration
df_clean = pd.concat([df_clean, df_clean.iloc[:5]], ignore_index=True)
print(f"Shape before removing duplicates: {df_clean.shape}")

# Remove duplicates
df_clean = cleaning.remove_duplicates(df_clean)
print(f"Shape after removing duplicates: {df_clean.shape}")

# Step 7: Handle outliers
print("\n=== Step 7: Handle Outliers ===")
# Add some outliers for demonstration
df_clean.loc[0, "numeric_column_1"] = 1000  # Far from the mean of ~50
df_clean.loc[1, "numeric_column_2"] = 500   # Far from the mean of ~10

# Detect outliers
from dshelpertool import stats
outliers, outlier_counts = stats.outlier_detection(df_clean,
                                                 cols=["numeric_column_1", "numeric_column_2"],
                                                 method="iqr")

print("Outlier counts:")
for col, info in outlier_counts.items():
    print(f"- {col}: {info['outlier_count']} outliers ({info['outlier_percentage']:.2f}%)")

# Replace outliers with column median
for col in ["numeric_column_1", "numeric_column_2"]:
    median_val = df_clean[col].median()
    df_clean.loc[outliers[col], col] = median_val

print("Outliers replaced with median values")

# Final result
print("\n=== Final Cleaned DataFrame ===")
print(df_clean.head())
print("\nData Types:")
print(df_clean.dtypes)
print("\nMissing Values:")
print(df_clean.isnull().sum())

print("\nData cleaning completed successfully!")
