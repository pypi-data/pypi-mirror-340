"""
Report module for generating reports and summaries.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


def generate_summary_report(df, title="Data Summary Report", include_plots=True, 
                           output_format="html", output_path=None):
    """
    Generate a comprehensive summary report for a DataFrame.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    title : str, default="Data Summary Report"
        Title of the report.
    include_plots : bool, default=True
        Whether to include plots in the report.
    output_format : str, default="html"
        Format of the output report: "html", "markdown", or "text".
    output_path : str or None, default=None
        Path to save the report. If None, returns the report as a string.
        
    Returns:
    -------
    str or None
        If output_path is None, returns the report as a string.
        Otherwise, saves the report to the specified path and returns None.
    """
    # Import necessary modules
    from dshelper import overview, eda, stats
    
    # Create report content
    if output_format == "html":
        report = _generate_html_report(df, title, include_plots)
    elif output_format == "markdown":
        report = _generate_markdown_report(df, title, include_plots)
    else:  # text
        report = _generate_text_report(df, title, include_plots)
    
    # Save or return report
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved to {output_path}")
        return None
    else:
        return report


def _generate_html_report(df, title, include_plots):
    """Generate HTML report."""
    from dshelper import overview, eda
    
    # Get basic statistics
    summary = overview.quick_look(df, name=title, include_describe=True, include_info=False)
    
    # Start building HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1, h2, h3 {{ color: #2c3e50; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            .missing {{ color: red; }}
            .container {{ margin-bottom: 30px; }}
            .plot-container {{ text-align: center; margin: 20px 0; }}
            .plot {{ max-width: 100%; height: auto; }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        <p>Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="container">
            <h2>Dataset Overview</h2>
            <p><strong>Shape:</strong> {df.shape[0]} rows × {df.shape[1]} columns</p>
            <p><strong>Memory Usage:</strong> {df.memory_usage(deep=True).sum() / (1024*1024):.2f} MB</p>
            
            <h3>Column Information</h3>
            <table>
                <tr>
                    <th>Column</th>
                    <th>Type</th>
                    <th>Non-Null Count</th>
                    <th>Missing</th>
                    <th>Missing %</th>
                    <th>Unique Values</th>
                </tr>
    """
    
    # Add column information
    for col in df.columns:
        dtype = str(df[col].dtype)
        non_null = df[col].count()
        missing = df[col].isna().sum()
        missing_pct = missing / len(df) * 100
        unique = df[col].nunique()
        
        html += f"""
                <tr>
                    <td>{col}</td>
                    <td>{dtype}</td>
                    <td>{non_null}</td>
                    <td class="{'missing' if missing > 0 else ''}">{missing}</td>
                    <td class="{'missing' if missing > 0 else ''}">{missing_pct:.2f}%</td>
                    <td>{unique}</td>
                </tr>
        """
    
    html += """
            </table>
        </div>
    """
    
    # Add numeric statistics
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        html += """
        <div class="container">
            <h2>Numeric Columns Statistics</h2>
            <table>
                <tr>
                    <th>Column</th>
                    <th>Mean</th>
                    <th>Std</th>
                    <th>Min</th>
                    <th>25%</th>
                    <th>50%</th>
                    <th>75%</th>
                    <th>Max</th>
                </tr>
        """
        
        desc = df[numeric_cols].describe().transpose()
        for col in desc.index:
            html += f"""
                <tr>
                    <td>{col}</td>
                    <td>{desc.loc[col, 'mean']:.4f}</td>
                    <td>{desc.loc[col, 'std']:.4f}</td>
                    <td>{desc.loc[col, 'min']:.4f}</td>
                    <td>{desc.loc[col, '25%']:.4f}</td>
                    <td>{desc.loc[col, '50%']:.4f}</td>
                    <td>{desc.loc[col, '75%']:.4f}</td>
                    <td>{desc.loc[col, 'max']:.4f}</td>
                </tr>
            """
        
        html += """
            </table>
        </div>
        """
    
    # Add categorical statistics
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    if len(cat_cols) > 0:
        html += """
        <div class="container">
            <h2>Categorical Columns Statistics</h2>
        """
        
        for col in cat_cols:
            value_counts = df[col].value_counts(dropna=False).head(5)
            
            html += f"""
            <h3>{col}</h3>
            <table>
                <tr>
                    <th>Value</th>
                    <th>Count</th>
                    <th>Percentage</th>
                </tr>
            """
            
            for val, count in value_counts.items():
                pct = count / len(df) * 100
                val_str = str(val) if pd.notna(val) else "NaN"
                html += f"""
                <tr>
                    <td>{val_str}</td>
                    <td>{count}</td>
                    <td>{pct:.2f}%</td>
                </tr>
                """
            
            html += """
            </table>
            """
        
        html += """
        </div>
        """
    
    # Add plots if requested
    if include_plots:
        html += """
        <div class="container">
            <h2>Data Visualizations</h2>
            
            <div class="plot-container">
                <h3>Missing Values</h3>
                <!-- Missing values plot would be embedded here -->
            </div>
            
            <div class="plot-container">
                <h3>Numeric Distributions</h3>
                <!-- Distribution plots would be embedded here -->
            </div>
            
            <div class="plot-container">
                <h3>Correlation Matrix</h3>
                <!-- Correlation matrix would be embedded here -->
            </div>
        </div>
        """
    
    # Close HTML
    html += """
    </body>
    </html>
    """
    
    return html


def _generate_markdown_report(df, title, include_plots):
    """Generate Markdown report."""
    from dshelper import overview, eda
    
    # Get basic statistics
    summary = overview.quick_look(df, name=title, include_describe=True, include_info=False)
    
    # Start building Markdown
    md = f"""# {title}

Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Dataset Overview

- **Shape:** {df.shape[0]} rows × {df.shape[1]} columns
- **Memory Usage:** {df.memory_usage(deep=True).sum() / (1024*1024):.2f} MB

### Column Information

| Column | Type | Non-Null Count | Missing | Missing % | Unique Values |
|--------|------|---------------|---------|-----------|---------------|
"""
    
    # Add column information
    for col in df.columns:
        dtype = str(df[col].dtype)
        non_null = df[col].count()
        missing = df[col].isna().sum()
        missing_pct = missing / len(df) * 100
        unique = df[col].nunique()
        
        md += f"| {col} | {dtype} | {non_null} | {missing} | {missing_pct:.2f}% | {unique} |\n"
    
    # Add numeric statistics
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        md += """
## Numeric Columns Statistics

| Column | Mean | Std | Min | 25% | 50% | 75% | Max |
|--------|------|-----|-----|-----|-----|-----|-----|
"""
        
        desc = df[numeric_cols].describe().transpose()
        for col in desc.index:
            md += f"| {col} | {desc.loc[col, 'mean']:.4f} | {desc.loc[col, 'std']:.4f} | {desc.loc[col, 'min']:.4f} | {desc.loc[col, '25%']:.4f} | {desc.loc[col, '50%']:.4f} | {desc.loc[col, '75%']:.4f} | {desc.loc[col, 'max']:.4f} |\n"
    
    # Add categorical statistics
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    if len(cat_cols) > 0:
        md += "\n## Categorical Columns Statistics\n"
        
        for col in cat_cols:
            value_counts = df[col].value_counts(dropna=False).head(5)
            
            md += f"\n### {col}\n\n"
            md += "| Value | Count | Percentage |\n"
            md += "|-------|-------|------------|\n"
            
            for val, count in value_counts.items():
                pct = count / len(df) * 100
                val_str = str(val) if pd.notna(val) else "NaN"
                md += f"| {val_str} | {count} | {pct:.2f}% |\n"
    
    # Add plots if requested
    if include_plots:
        md += """
## Data Visualizations

### Missing Values
(Missing values plot would be included here)

### Numeric Distributions
(Distribution plots would be included here)

### Correlation Matrix
(Correlation matrix would be included here)
"""
    
    return md


def _generate_text_report(df, title, include_plots):
    """Generate plain text report."""
    from dshelper import overview, eda
    
    # Get basic statistics
    summary = overview.quick_look(df, name=title, include_describe=True, include_info=False)
    
    # Start building text report
    text = f"""{title}
{'=' * len(title)}

Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Dataset Overview
---------------
Shape: {df.shape[0]} rows × {df.shape[1]} columns
Memory Usage: {df.memory_usage(deep=True).sum() / (1024*1024):.2f} MB

Column Information:
"""
    
    # Add column information
    for col in df.columns:
        dtype = str(df[col].dtype)
        non_null = df[col].count()
        missing = df[col].isna().sum()
        missing_pct = missing / len(df) * 100
        unique = df[col].nunique()
        
        text += f"- {col} ({dtype}): {non_null} non-null, {missing} missing ({missing_pct:.2f}%), {unique} unique values\n"
    
    # Add numeric statistics
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        text += "\nNumeric Columns Statistics:\n"
        text += "--------------------------\n"
        
        desc = df[numeric_cols].describe().transpose()
        for col in desc.index:
            text += f"{col}:\n"
            text += f"  Mean: {desc.loc[col, 'mean']:.4f}\n"
            text += f"  Std: {desc.loc[col, 'std']:.4f}\n"
            text += f"  Min: {desc.loc[col, 'min']:.4f}\n"
            text += f"  25%: {desc.loc[col, '25%']:.4f}\n"
            text += f"  50%: {desc.loc[col, '50%']:.4f}\n"
            text += f"  75%: {desc.loc[col, '75%']:.4f}\n"
            text += f"  Max: {desc.loc[col, 'max']:.4f}\n\n"
    
    # Add categorical statistics
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    if len(cat_cols) > 0:
        text += "\nCategorical Columns Statistics:\n"
        text += "------------------------------\n"
        
        for col in cat_cols:
            value_counts = df[col].value_counts(dropna=False).head(5)
            
            text += f"\n{col}:\n"
            for val, count in value_counts.items():
                pct = count / len(df) * 100
                val_str = str(val) if pd.notna(val) else "NaN"
                text += f"  {val_str}: {count} ({pct:.2f}%)\n"
    
    # Add plots if requested
    if include_plots:
        text += "\nData Visualizations:\n"
        text += "-------------------\n"
        text += "Note: Visualizations are not available in text format.\n"
        text += "Please use HTML or Markdown format to include visualizations.\n"
    
    return text


def export_to_excel(df, filename, include_summary=True, include_plots=False):
    """
    Export DataFrame to Excel with optional summary sheet and plots.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    filename : str
        Path to save the Excel file.
    include_summary : bool, default=True
        Whether to include a summary sheet.
    include_plots : bool, default=False
        Whether to include plots in the Excel file.
        
    Returns:
    -------
    None
    """
    try:
        import openpyxl
        from openpyxl.utils.dataframe import dataframe_to_rows
        from openpyxl.drawing.image import Image
        import io
    except ImportError:
        print("Error: This function requires openpyxl. Install it with 'pip install openpyxl'.")
        return
    
    # Create Excel writer
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Write data to 'Data' sheet
        df.to_excel(writer, sheet_name='Data', index=True)
        
        # Add summary sheet if requested
        if include_summary:
            # Create summary DataFrame
            summary_data = {
                'Column': [],
                'Type': [],
                'Non-Null Count': [],
                'Missing': [],
                'Missing %': [],
                'Unique Values': []
            }
            
            for col in df.columns:
                summary_data['Column'].append(col)
                summary_data['Type'].append(str(df[col].dtype))
                summary_data['Non-Null Count'].append(df[col].count())
                summary_data['Missing'].append(df[col].isna().sum())
                summary_data['Missing %'].append(df[col].isna().mean() * 100)
                summary_data['Unique Values'].append(df[col].nunique())
            
            summary_df = pd.DataFrame(summary_data)
            
            # Write summary to 'Summary' sheet
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Add numeric statistics if there are numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                desc = df[numeric_cols].describe().transpose().reset_index()
                desc.columns = ['Column'] + list(desc.columns[1:])
                desc.to_excel(writer, sheet_name='Numeric Stats', index=False)
            
            # Add categorical statistics if there are categorical columns
            cat_cols = df.select_dtypes(include=['object', 'category']).columns
            if len(cat_cols) > 0:
                # Create a new sheet for each categorical column
                for col in cat_cols:
                    value_counts = df[col].value_counts(dropna=False).reset_index()
                    value_counts.columns = [col, 'Count']
                    value_counts['Percentage'] = value_counts['Count'] / len(df) * 100
                    
                    # Limit to top 100 values to avoid Excel limitations
                    value_counts = value_counts.head(100)
                    
                    # Write to sheet (use first 30 chars of column name to avoid Excel sheet name limitations)
                    sheet_name = f"{col[:30]}_counts"
                    value_counts.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Add plots if requested
        if include_plots:
            print("Note: Adding plots to Excel is not fully implemented yet.")
            # This would require additional code to create and save plots to the Excel file
    
    print(f"Excel file saved to {filename}")


def generate_data_dictionary(df, filename=None, include_stats=True):
    """
    Generate a data dictionary for a DataFrame.
    
    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    filename : str or None, default=None
        Path to save the data dictionary. If None, returns the dictionary as a DataFrame.
    include_stats : bool, default=True
        Whether to include basic statistics in the dictionary.
        
    Returns:
    -------
    pandas.DataFrame or None
        If filename is None, returns the data dictionary as a DataFrame.
        Otherwise, saves the dictionary to the specified file and returns None.
    """
    # Create data dictionary
    data_dict = {
        'Column': [],
        'Type': [],
        'Description': [],
        'Non-Null Count': [],
        'Missing': [],
        'Missing %': [],
        'Unique Values': []
    }
    
    # Add basic statistics if requested
    if include_stats:
        data_dict.update({
            'Min': [],
            'Max': [],
            'Mean': [],
            'Median': [],
            'Std': [],
            'Example Values': []
        })
    
    # Fill dictionary
    for col in df.columns:
        data_dict['Column'].append(col)
        data_dict['Type'].append(str(df[col].dtype))
        data_dict['Description'].append('')  # Empty description to be filled by user
        data_dict['Non-Null Count'].append(df[col].count())
        data_dict['Missing'].append(df[col].isna().sum())
        data_dict['Missing %'].append(df[col].isna().mean() * 100)
        data_dict['Unique Values'].append(df[col].nunique())
        
        if include_stats:
            # Add statistics for numeric columns
            if pd.api.types.is_numeric_dtype(df[col]):
                data_dict['Min'].append(df[col].min())
                data_dict['Max'].append(df[col].max())
                data_dict['Mean'].append(df[col].mean())
                data_dict['Median'].append(df[col].median())
                data_dict['Std'].append(df[col].std())
            else:
                data_dict['Min'].append(None)
                data_dict['Max'].append(None)
                data_dict['Mean'].append(None)
                data_dict['Median'].append(None)
                data_dict['Std'].append(None)
            
            # Add example values
            example_values = df[col].dropna().sample(min(3, df[col].count())).tolist()
            data_dict['Example Values'].append(', '.join(str(val) for val in example_values))
    
    # Create DataFrame
    data_dict_df = pd.DataFrame(data_dict)
    
    # Save to file if filename is provided
    if filename:
        if filename.endswith('.csv'):
            data_dict_df.to_csv(filename, index=False)
        elif filename.endswith('.xlsx'):
            data_dict_df.to_excel(filename, index=False)
        else:
            data_dict_df.to_csv(filename, index=False)
        
        print(f"Data dictionary saved to {filename}")
        return None
    else:
        return data_dict_df
