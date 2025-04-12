"""
Tests for the overview module.
"""
import unittest
import pandas as pd
import numpy as np
from dshelpertool import overview


class TestOverview(unittest.TestCase):
    """Tests for the overview module."""

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

    def test_quick_look(self):
        """Test the quick_look function."""
        # Test with default parameters
        result = overview.quick_look(self.df, name="Test DataFrame")

        # Check that the result is a dictionary
        self.assertIsInstance(result, dict)

        # Check that the dictionary contains the expected keys
        expected_keys = ['name', 'shape', 'columns', 'dtypes', 'missing_values',
                         'missing_percentage', 'unique_values', 'describe']
        for key in expected_keys:
            self.assertIn(key, result)

        # Check that the shape is correct
        self.assertEqual(result['shape'], (5, 5))

        # Check that the columns are correct
        self.assertEqual(result['columns'], ['A', 'B', 'C', 'D', 'E'])

    def test_get_duplicates(self):
        """Test the get_duplicates function."""
        # Create a DataFrame with duplicates
        df_with_duplicates = pd.DataFrame({
            'A': [1, 2, 3, 1, 2],
            'B': [1.1, 2.2, 3.3, 1.1, 2.2],
            'C': ['a', 'b', 'c', 'a', 'b']
        })

        # Test with default parameters
        result = overview.get_duplicates(df_with_duplicates)

        # Check that the result is a DataFrame
        self.assertIsInstance(result, pd.DataFrame)

        # Check that the result has the expected shape
        self.assertEqual(result.shape, (2, 3))

        # Test with subset parameter
        result = overview.get_duplicates(df_with_duplicates, subset=['A'])

        # Check that the result has the expected shape
        self.assertEqual(result.shape, (2, 3))

        # Test with keep parameter
        result = overview.get_duplicates(df_with_duplicates, keep='last')

        # Check that the result has the expected shape
        self.assertEqual(result.shape, (2, 3))

        # Test with no duplicates
        result = overview.get_duplicates(self.df)

        # Check that the result is an empty DataFrame
        self.assertEqual(result.shape[0], 0)

    def test_value_counts_all(self):
        """Test the value_counts_all function."""
        # Test with default parameters
        result = overview.value_counts_all(self.df)

        # Check that the result is a dictionary
        self.assertIsInstance(result, dict)

        # Check that the dictionary contains the expected keys
        self.assertIn('C', result)

        # Check that the value for 'C' is a DataFrame
        self.assertIsInstance(result['C'], pd.DataFrame)

        # Check that the DataFrame has the expected shape
        self.assertEqual(result['C'].shape, (5, 3))

        # Test with top_n parameter
        result = overview.value_counts_all(self.df, top_n=3)

        # Check that the DataFrame has the expected shape
        self.assertEqual(result['C'].shape, (3, 3))

    def test_column_info(self):
        """Test the column_info function."""
        # Test with default parameters
        result = overview.column_info(self.df)

        # Check that the result is a dictionary
        self.assertIsInstance(result, dict)

        # Check that the dictionary contains the expected keys
        for col in self.df.columns:
            self.assertIn(col, result)

        # Check that each value is a dictionary
        for col in result:
            self.assertIsInstance(result[col], dict)

        # Test with column parameter
        result = overview.column_info(self.df, column='A')

        # Check that the result contains only the specified column
        self.assertEqual(list(result.keys()), ['A'])

        # Check that the dictionary contains the expected keys
        expected_keys = ['dtype', 'count', 'missing', 'missing_percentage', 'unique_values',
                         'min', 'max', 'mean', 'median', 'std', 'zeros', 'zeros_percentage',
                         'negative_values', 'negative_percentage']
        for key in expected_keys:
            self.assertIn(key, result['A'])

    def test_find_outliers(self):
        """Test the find_outliers function."""
        # Create a DataFrame with outliers
        df_with_outliers = pd.DataFrame({
            'A': [1, 2, 3, 4, 100],
            'B': [1.1, 2.2, 3.3, 4.4, 5.5]
        })

        # Test with default parameters
        result = overview.find_outliers(df_with_outliers)

        # Check that the result is a dictionary
        self.assertIsInstance(result, dict)

        # Check that the dictionary contains the expected keys
        self.assertIn('A', result)

        # Check that the value for 'A' is a DataFrame
        self.assertIsInstance(result['A'], pd.DataFrame)

        # Check that the DataFrame has the expected shape
        self.assertEqual(result['A'].shape[0], 1)

        # Test with method parameter
        result = overview.find_outliers(df_with_outliers, method='zscore')

        # Check that the result is a dictionary
        self.assertIsInstance(result, dict)

        # Test with threshold parameter
        result = overview.find_outliers(df_with_outliers, threshold=3)

        # Check that the result is a dictionary
        self.assertIsInstance(result, dict)


if __name__ == '__main__':
    unittest.main()
