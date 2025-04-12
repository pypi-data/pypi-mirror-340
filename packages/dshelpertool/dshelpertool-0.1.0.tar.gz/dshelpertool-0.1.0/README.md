# DSHelperTool

A lightweight helper package for data science and analysis tasks. DSHelperTool aims to reduce the hassle of common data analysis tasks by 80-90% with simple, intuitive functions.

## Installation

```bash
pip install dshelpertool
```

## Features

- **Quick Data Overview**: Get a comprehensive summary of your DataFrame with a single function call
- **Data Cleaning**: Easily standardize column names, handle missing values, and fix data types
- **Exploratory Data Analysis**: Analyze distributions, correlations, and patterns in your data
- **Visualization**: Create informative plots with minimal code
- **Data Type Handling**: Convert columns to appropriate data types with smart error handling

## Usage Examples

### Quick Overview of a DataFrame

```python
import pandas as pd
from dshelpertool import overview as ov

# Load your data
df = pd.read_csv("your_data.csv")

# Get a comprehensive overview
ov.quick_look(df, name="My Dataset")
```

### Clean Column Names

```python
from dshelpertool import cleaning as cl

# Standardize all column names (lowercase with underscores)
df = cl.update_col(df, standardize_col=True)

# Or rename specific columns
df = cl.update_col(df, rename_dict={"Old Name": "new_name", "Another Column": "another_column"})
```

### Handle Data Types

```python
from dshelpertool import dtypes as dt

# Convert columns to numeric
df = dt.to_numeric_cols(df, ["quantity", "price", "amount"])

# Convert columns to datetime
df = dt.to_datetime_cols(df, "transaction_date")
```

### Analyze Categorical Data

```python
from dshelpertool import overview as ov

# Get value counts for all categorical columns
result = ov.value_counts_all(df, top_n=5)

# Visualize the distributions
ov.plot_value_counts(df, columns=["category", "status"], top_n=5)
```

### Check for Skewness

```python
from dshelpertool import eda

# Check skewness of numeric columns
eda.check_skew(df, cols=["price", "quantity"])

# Visualize the distributions
eda.plot_skew(df, cols=["price", "quantity"])
```

## Development

### Setting up the Development Environment

```bash
# Clone the repository
git clone https://github.com/uumap/dshelpertool.git
cd dshelpertool

# Install in development mode with development dependencies
pip install -e .[dev]

# Run tests
python -m pytest
```

### GitHub Actions Workflows

This project uses GitHub Actions for continuous integration and deployment:

1. **Python Tests** (`python-test.yml`): Runs on every push to main and pull request
   - Runs tests on multiple Python versions
   - Performs linting with flake8
   - Checks code formatting with black
   - Checks import order with isort
   - Reports test coverage

2. **Publish Python Package** (`python-publish.yml`): Runs when a new release is created
   - Tests the package on multiple Python versions
   - Builds the package
   - Publishes to PyPI

To manually trigger the test workflow, go to the Actions tab in your GitHub repository and select "Python Tests" workflow, then click "Run workflow".

## Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the tests (`pytest`)
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
