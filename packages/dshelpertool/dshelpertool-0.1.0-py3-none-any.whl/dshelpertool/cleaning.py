"""
Cleaning module for data preprocessing and cleaning.
"""
import pandas as pd


def update_col(df, rename_dict=None, standardize_col=False):
    """
    Rename columns or standardize all column names.

    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    rename_dict : dict, optional
        Mapping of current column names to new ones, e.g., {'Old Name': 'new_name'}
    standardize_col : bool, optional
        If True, standardize all column names to lowercase with underscores.

    Returns:
    -------
    pandas.DataFrame
        DataFrame with updated column names.
    """
    if standardize_col:
        df = df.rename(columns=lambda x: str(x).strip().lower().replace(" ", "_"))
    elif rename_dict:
        df = df.rename(columns=rename_dict)
    else:
        raise ValueError(
            "Provide either 'standardize_col=True' or a 'rename_dict' mapping."
        )
    return df


def drop_cols(df, cols=None):
    """
    Drop specified columns from a DataFrame.

    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    cols : str or list, optional
        Column name or list of column names to drop.
        If None, all columns will be dropped.

    Returns:
    -------
    pandas.DataFrame
        DataFrame with the specified columns removed.

    Example:
    -------
    >>> drop_cols(df, 'age')
    >>> drop_cols(df, ['age', 'salary'])
    >>> drop_cols(df)  # drops all columns
    """
    if cols is None:
        cols = df.columns
    elif isinstance(cols, str):
        cols = [cols]

    return df.drop(columns=cols, errors='ignore')


def drop_missing(df, axis=0, thresh=None, subset=None, how='any'):
    """
    Drop rows or columns with missing values.

    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    axis : {0 or 'index', 1 or 'columns'}, default=0
        Determine if rows or columns are dropped:
        - 0 or 'index': Drop rows
        - 1 or 'columns': Drop columns
    thresh : int, optional
        Require that many non-NA values. If None, drops based on 'how' parameter.
    subset : list, optional
        List of column labels to consider for dropping rows.
    how : {'any', 'all'}, default='any'
        Determine if row or column is removed:
        - 'any': If any NA values are present
        - 'all': If all values are NA

    Returns:
    -------
    pandas.DataFrame
        DataFrame with rows or columns dropped.
    """
    # Count missing values before dropping
    if axis == 0 or axis == 'index':
        missing_before = df.isnull().sum(axis=1).sum()
    else:
        missing_before = df.isnull().sum().sum()

    # Drop missing values
    if thresh is not None:
        df_cleaned = df.dropna(axis=axis, thresh=thresh, subset=subset)
    else:
        df_cleaned = df.dropna(axis=axis, subset=subset, how=how)

    # Count missing values after dropping
    if axis == 0 or axis == 'index':
        missing_after = df_cleaned.isnull().sum(axis=1).sum()
        dropped_count = df.shape[0] - df_cleaned.shape[0]
        print(f"Dropped {dropped_count} rows ({dropped_count/df.shape[0]*100:.2f}% of total rows)")
    else:
        missing_after = df_cleaned.isnull().sum().sum()
        dropped_count = df.shape[1] - df_cleaned.shape[1]
        print(f"Dropped {dropped_count} columns ({dropped_count/df.shape[1]*100:.2f}% of total columns)")

    print(f"Missing values before: {missing_before}")
    print(f"Missing values after: {missing_after}")
    print(f"Reduction in missing values: {missing_before - missing_after} ({(missing_before - missing_after)/missing_before*100:.2f}% of total missing)")

    return df_cleaned


def remove_duplicates(df, subset=None, keep='first', inplace=False):
    """
    Remove duplicate rows from a DataFrame.

    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    subset : list, optional
        List of column labels to consider for identifying duplicates.
        If None, use all columns.
    keep : {'first', 'last', False}, default='first'
        Which duplicates to keep:
        - 'first': Keep first occurrence
        - 'last': Keep last occurrence
        - False: Drop all duplicates
    inplace : bool, default=False
        Whether to modify the DataFrame in place.

    Returns:
    -------
    pandas.DataFrame
        DataFrame with duplicates removed.
    """
    # Count duplicates before removing
    if subset is not None:
        if isinstance(subset, str):
            subset = [subset]
        missing_cols = [col for col in subset if col not in df.columns]
        if missing_cols:
            print(f"Warning: Columns {missing_cols} not found in DataFrame.")
            print(f"Available columns: {df.columns.tolist()}")
            return df

    dup_count = df.duplicated(subset=subset, keep=False).sum()

    if dup_count == 0:
        print("No duplicates found.")
        return df

    # Remove duplicates
    df_cleaned = df.drop_duplicates(subset=subset, keep=keep, inplace=inplace)

    if inplace:
        df_cleaned = df

    # Print summary
    removed_count = dup_count - (df.duplicated(subset=subset, keep=False).sum() if keep else 0)
    print(f"Found {dup_count} duplicate rows ({dup_count/df.shape[0]*100:.2f}% of total rows)")
    print(f"Removed {removed_count} rows")
    print(f"Rows before: {df.shape[0]}")
    print(f"Rows after: {df_cleaned.shape[0]}")

    return df_cleaned


def replace_values(df, columns=None, to_replace=None, value=None, regex=False):
    """
    Replace values in specified columns.

    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    columns : str or list, optional
        Column name or list of column names to replace values in.
        If None, replace in all columns.
    to_replace : str, list, dict, or scalar, default=None
        Values to be replaced. Various forms accepted.
    value : str, list, dict, or scalar, default=None
        Values to replace with. Various forms accepted.
    regex : bool, default=False
        Whether to interpret to_replace as a regular expression.

    Returns:
    -------
    pandas.DataFrame
        DataFrame with replaced values.
    """
    if columns is None:
        columns = df.columns
    elif isinstance(columns, str):
        columns = [columns]

    # Check if columns exist
    missing_cols = [col for col in columns if col not in df.columns]
    if missing_cols:
        print(f"Warning: Columns {missing_cols} not found in DataFrame.")
        print(f"Available columns: {df.columns.tolist()}")
        columns = [col for col in columns if col in df.columns]

    # Replace values
    df_cleaned = df.copy()
    for col in columns:
        df_cleaned[col] = df_cleaned[col].replace(to_replace=to_replace, value=value, regex=regex)

    # Print summary
    changed_count = (df[columns] != df_cleaned[columns]).sum().sum()
    print(f"Changed {changed_count} values across {len(columns)} columns")

    return df_cleaned


def clean_text(df, columns=None, lower=True, strip=True, remove_special=False,
               remove_numbers=False, remove_extra_spaces=True):
    """
    Clean text data in specified columns.

    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    columns : str or list, optional
        Column name or list of column names to clean.
        If None, clean all string columns.
    lower : bool, default=True
        Convert text to lowercase.
    strip : bool, default=True
        Remove leading and trailing whitespace.
    remove_special : bool, default=False
        Remove special characters.
    remove_numbers : bool, default=False
        Remove numbers.
    remove_extra_spaces : bool, default=True
        Replace multiple spaces with a single space.

    Returns:
    -------
    pandas.DataFrame
        DataFrame with cleaned text.
    """

    # Select columns to clean
    if columns is None:
        columns = df.select_dtypes(include=['object']).columns
    elif isinstance(columns, str):
        columns = [columns]

    # Check if columns exist
    missing_cols = [col for col in columns if col not in df.columns]
    if missing_cols:
        print(f"Warning: Columns {missing_cols} not found in DataFrame.")
        print(f"Available columns: {df.columns.tolist()}")
        columns = [col for col in columns if col in df.columns]

    # Clean text
    df_cleaned = df.copy()
    for col in columns:
        # Skip non-string columns
        if df_cleaned[col].dtype != 'object':
            print(f"Skipping non-string column: {col} (dtype: {df_cleaned[col].dtype})")
            continue

        # Apply cleaning operations
        if lower:
            df_cleaned[col] = df_cleaned[col].str.lower()

        if strip:
            df_cleaned[col] = df_cleaned[col].str.strip()

        if remove_special:
            df_cleaned[col] = df_cleaned[col].str.replace(r'[^\w\s]', '', regex=True)

        if remove_numbers:
            df_cleaned[col] = df_cleaned[col].str.replace(r'\d+', '', regex=True)

        if remove_extra_spaces:
            df_cleaned[col] = df_cleaned[col].str.replace(r'\s+', ' ', regex=True)

    # Print summary
    print(f"Cleaned text in {len(columns)} columns")

    return df_cleaned


def fix_data_types(df, infer_types=True, numeric_cols=None, datetime_cols=None,
                   category_cols=None, text_cols=None):
    """
    Fix data types in a DataFrame.

    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    infer_types : bool, default=True
        Whether to automatically infer data types.
    numeric_cols : list, optional
        List of columns to convert to numeric.
    datetime_cols : list, optional
        List of columns to convert to datetime.
    category_cols : list, optional
        List of columns to convert to categorical.
    text_cols : list, optional
        List of columns to ensure are string type.

    Returns:
    -------
    pandas.DataFrame
        DataFrame with fixed data types.
    """
    from pandas.api.types import is_numeric_dtype, is_datetime64_any_dtype

    df_fixed = df.copy()
    changes = []

    # Automatically infer data types
    if infer_types:
        for col in df.columns:
            # Skip columns that are already correctly typed
            if col in (numeric_cols or []) or col in (datetime_cols or []) or \
               col in (category_cols or []) or col in (text_cols or []):
                continue

            # Try to convert to numeric
            if not is_numeric_dtype(df[col]):
                try:
                    numeric_series = pd.to_numeric(df[col], errors='coerce')
                    # If more than 80% of values are valid numbers, convert to numeric
                    if numeric_series.notna().mean() > 0.8:
                        df_fixed[col] = numeric_series
                        changes.append(f"{col}: object -> numeric")
                        continue
                except:
                    pass

            # Try to convert to datetime
            if not is_datetime64_any_dtype(df[col]):
                try:
                    datetime_series = pd.to_datetime(df[col], errors='coerce')
                    # If more than 80% of values are valid dates, convert to datetime
                    if datetime_series.notna().mean() > 0.8:
                        df_fixed[col] = datetime_series
                        changes.append(f"{col}: object -> datetime")
                        continue
                except:
                    pass

            # Check if column should be categorical
            if df[col].dtype == 'object':
                # If column has few unique values relative to total rows, convert to categorical
                if df[col].nunique() / len(df) < 0.1:
                    df_fixed[col] = df[col].astype('category')
                    changes.append(f"{col}: object -> category")

    # Convert specified columns to numeric
    if numeric_cols:
        for col in numeric_cols:
            if col in df.columns:
                old_dtype = df[col].dtype
                df_fixed[col] = pd.to_numeric(df[col], errors='coerce')
                changes.append(f"{col}: {old_dtype} -> numeric")
            else:
                print(f"Warning: Column '{col}' not found in DataFrame.")

    # Convert specified columns to datetime
    if datetime_cols:
        for col in datetime_cols:
            if col in df.columns:
                old_dtype = df[col].dtype
                df_fixed[col] = pd.to_datetime(df[col], errors='coerce')
                changes.append(f"{col}: {old_dtype} -> datetime")
            else:
                print(f"Warning: Column '{col}' not found in DataFrame.")

    # Convert specified columns to categorical
    if category_cols:
        for col in category_cols:
            if col in df.columns:
                old_dtype = df[col].dtype
                df_fixed[col] = df[col].astype('category')
                changes.append(f"{col}: {old_dtype} -> category")
            else:
                print(f"Warning: Column '{col}' not found in DataFrame.")

    # Convert specified columns to string
    if text_cols:
        for col in text_cols:
            if col in df.columns:
                old_dtype = df[col].dtype
                df_fixed[col] = df[col].astype(str)
                changes.append(f"{col}: {old_dtype} -> string")
            else:
                print(f"Warning: Column '{col}' not found in DataFrame.")

    # Print summary
    if changes:
        print("Data type changes:")
        for change in changes:
            print(f"- {change}")
    else:
        print("No data type changes made.")

    return df_fixed
