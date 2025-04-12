"""
Tests for the cleaning module.
"""
import unittest
import pandas as pd
import numpy as np
from dshelpertool import cleaning


class TestCleaning(unittest.TestCase):
    """Tests for the cleaning module."""

    def setUp(self):
        """Set up test data."""
        # Create a sample DataFrame for testing
        self.df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [1.1, 2.2, 3.3, 4.4, 5.5],
            'C': ['a', 'b', 'c', 'd', 'e'],
            'D': [True, False, True, False, True],
            'E': pd.date_range('2021-01-01', periods=5)
        })

        # Add some missing values
        self.df_with_missing = self.df.copy()
        self.df_with_missing.loc[0, 'A'] = np.nan
        self.df_with_missing.loc[1, 'B'] = np.nan
        self.df_with_missing.loc[2, 'C'] = np.nan

        # Create a DataFrame with messy column names
        self.df_messy_cols = pd.DataFrame({
            'First Name': ['John', 'Jane', 'Bob'],
            'Last Name': ['Doe', 'Smith', 'Johnson'],
            'Age ': [25, 30, 35],
            ' Email': ['john@example.com', 'jane@example.com', 'bob@example.com']
        })

    def test_update_col(self):
        """Test the update_col function."""
        # Test with standardize_col=True
        result = cleaning.update_col(self.df_messy_cols, standardize_col=True)

        # Check that the result is a DataFrame
        self.assertIsInstance(result, pd.DataFrame)

        # Check that the column names are standardized
        expected_cols = ['first_name', 'last_name', 'age', 'email']
        self.assertEqual(list(result.columns), expected_cols)

        # Test with rename_dict
        rename_dict = {'A': 'Alpha', 'B': 'Beta', 'C': 'Charlie'}
        result = cleaning.update_col(self.df, rename_dict=rename_dict)

        # Check that the column names are renamed
        expected_cols = ['Alpha', 'Beta', 'Charlie', 'D', 'E']
        self.assertEqual(list(result.columns), expected_cols)

        # Test with invalid parameters
        with self.assertRaises(ValueError):
            cleaning.update_col(self.df)

    def test_drop_cols(self):
        """Test the drop_cols function."""
        # Test with a single column
        result = cleaning.drop_cols(self.df, cols='A')

        # Check that the result is a DataFrame
        self.assertIsInstance(result, pd.DataFrame)

        # Check that the column is dropped
        self.assertEqual(list(result.columns), ['B', 'C', 'D', 'E'])

        # Test with multiple columns
        result = cleaning.drop_cols(self.df, cols=['A', 'B'])

        # Check that the columns are dropped
        self.assertEqual(list(result.columns), ['C', 'D', 'E'])

        # Test with None
        result = cleaning.drop_cols(self.df, cols=None)

        # Check that all columns are dropped
        self.assertEqual(result.shape, (5, 0))

    def test_drop_missing(self):
        """Test the drop_missing function."""
        # Test with default parameters
        result = cleaning.drop_missing(self.df_with_missing)

        # Check that the result is a DataFrame
        self.assertIsInstance(result, pd.DataFrame)

        # Check that rows with missing values are dropped
        self.assertEqual(result.shape[0], 2)

        # Test with axis=1
        result = cleaning.drop_missing(self.df_with_missing, axis=1)

        # Check that columns with missing values are dropped
        self.assertEqual(result.shape[1], 2)

        # Test with how='all'
        result = cleaning.drop_missing(self.df_with_missing, how='all')

        # Check that no rows are dropped (no row has all missing values)
        self.assertEqual(result.shape[0], 5)

        # Test with subset
        result = cleaning.drop_missing(self.df_with_missing, subset=['A'])

        # Check that only rows with missing values in column A are dropped
        self.assertEqual(result.shape[0], 4)

    def test_remove_duplicates(self):
        """Test the remove_duplicates function."""
        # Create a DataFrame with duplicates
        df_with_duplicates = pd.DataFrame({
            'A': [1, 2, 3, 1, 2],
            'B': [1.1, 2.2, 3.3, 1.1, 2.2],
            'C': ['a', 'b', 'c', 'a', 'b']
        })

        # Test with default parameters
        result = cleaning.remove_duplicates(df_with_duplicates)

        # Check that the result is a DataFrame
        self.assertIsInstance(result, pd.DataFrame)

        # Check that duplicates are removed
        self.assertEqual(result.shape[0], 3)

        # Test with keep='last'
        result = cleaning.remove_duplicates(df_with_duplicates, keep='last')

        # Check that duplicates are removed
        self.assertEqual(result.shape[0], 3)

        # Test with keep=False
        result = cleaning.remove_duplicates(df_with_duplicates, keep=False)

        # Check that all duplicates are removed
        self.assertEqual(result.shape[0], 1)

        # Test with subset
        result = cleaning.remove_duplicates(df_with_duplicates, subset=['A'])

        # Check that duplicates based on subset are removed
        self.assertEqual(result.shape[0], 3)

    def test_replace_values(self):
        """Test the replace_values function."""
        # Test with to_replace and value
        result = cleaning.replace_values(self.df, to_replace=1, value=10)

        # Check that the result is a DataFrame
        self.assertIsInstance(result, pd.DataFrame)

        # Check that values are replaced
        self.assertEqual(result.loc[0, 'A'], 10)

        # Test with columns
        result = cleaning.replace_values(self.df, columns=['A'], to_replace=1, value=10)

        # Check that values are replaced only in the specified column
        self.assertEqual(result.loc[0, 'A'], 10)
        self.assertEqual(result.loc[0, 'B'], 1.1)

        # Test with regex
        result = cleaning.replace_values(self.df, columns=['C'], to_replace='[aeiou]', value='X', regex=True)

        # Check that values are replaced using regex
        self.assertEqual(result.loc[0, 'C'], 'X')

    def test_clean_text(self):
        """Test the clean_text function."""
        # Create a DataFrame with text data
        df_text = pd.DataFrame({
            'A': ['  Hello  ', 'World', '  Hello World  '],
            'B': ['123', '456', '789'],
            'C': ['Hello123', 'World456', 'Hello789World']
        })

        # Test with default parameters
        result = cleaning.clean_text(df_text)

        # Check that the result is a DataFrame
        self.assertIsInstance(result, pd.DataFrame)

        # Check that text is cleaned
        self.assertEqual(result.loc[0, 'A'], 'hello')

        # Test with specific parameters
        result = cleaning.clean_text(df_text, columns=['A'], lower=False, strip=True, remove_special=False)

        # Check that text is cleaned according to parameters
        self.assertEqual(result.loc[0, 'A'], 'Hello')

        # Test with remove_special=True
        result = cleaning.clean_text(df_text, columns=['C'], remove_special=True)

        # Check that special characters are removed
        self.assertEqual(result.loc[0, 'C'], 'hello123')

        # Test with remove_numbers=True
        result = cleaning.clean_text(df_text, columns=['C'], remove_numbers=True)

        # Check that numbers are removed
        self.assertEqual(result.loc[0, 'C'], 'hello')

    def test_fix_data_types(self):
        """Test the fix_data_types function."""
        # Create a DataFrame with mixed data types
        df_mixed = pd.DataFrame({
            'A': ['1', '2', '3', '4', '5'],
            'B': ['1.1', '2.2', '3.3', '4.4', '5.5'],
            'C': ['2021-01-01', '2021-01-02', '2021-01-03', '2021-01-04', '2021-01-05'],
            'D': ['true', 'false', 'true', 'false', 'true']
        })

        # Test with infer_types=True
        result = cleaning.fix_data_types(df_mixed)

        # Check that the result is a DataFrame
        self.assertIsInstance(result, pd.DataFrame)

        # Check that data types are fixed
        self.assertTrue(pd.api.types.is_numeric_dtype(result['A']))
        self.assertTrue(pd.api.types.is_numeric_dtype(result['B']))

        # Test with specific parameters
        result = cleaning.fix_data_types(df_mixed, infer_types=False, numeric_cols=['A', 'B'])

        # Check that data types are fixed according to parameters
        self.assertTrue(pd.api.types.is_numeric_dtype(result['A']))
        self.assertTrue(pd.api.types.is_numeric_dtype(result['B']))

        # Test with datetime_cols
        result = cleaning.fix_data_types(df_mixed, infer_types=False, datetime_cols=['C'])

        # Check that data types are fixed according to parameters
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(result['C']))


if __name__ == '__main__':
    unittest.main()
