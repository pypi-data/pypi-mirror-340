"""
Command-line interface for the dshelpertool package.
"""
import argparse
import os
import sys
import pandas as pd
from dshelpertool import __version__
from dshelpertool import overview, cleaning, dtypes, eda, stats, viz, report


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="DSHelperTool: A lightweight helper package for data science and analysis tasks."
    )

    # Add version argument
    parser.add_argument(
        "--version", action="version", version=f"dshelpertool {__version__}"
    )

    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Overview command
    overview_parser = subparsers.add_parser(
        "overview", help="Get a quick overview of a DataFrame"
    )
    overview_parser.add_argument(
        "file", help="Path to the CSV or Excel file"
    )
    overview_parser.add_argument(
        "--name", help="Name of the DataFrame", default="DataFrame"
    )

    # Clean command
    clean_parser = subparsers.add_parser(
        "clean", help="Clean a DataFrame"
    )
    clean_parser.add_argument(
        "file", help="Path to the CSV or Excel file"
    )
    clean_parser.add_argument(
        "--standardize", action="store_true", help="Standardize column names"
    )
    clean_parser.add_argument(
        "--output", help="Path to save the cleaned file", default=None
    )

    # Report command
    report_parser = subparsers.add_parser(
        "report", help="Generate a report for a DataFrame"
    )
    report_parser.add_argument(
        "file", help="Path to the CSV or Excel file"
    )
    report_parser.add_argument(
        "--title", help="Title of the report", default="Data Report"
    )
    report_parser.add_argument(
        "--format", choices=["html", "markdown", "text"], default="html",
        help="Format of the report"
    )
    report_parser.add_argument(
        "--output", help="Path to save the report", default=None
    )
    report_parser.add_argument(
        "--plots", action="store_true", help="Include plots in the report"
    )

    # Parse arguments
    args = parser.parse_args()

    # If no command is provided, print help
    if args.command is None:
        parser.print_help()
        return

    # Load the file
    try:
        if args.file.endswith(".csv"):
            df = pd.read_csv(args.file)
        elif args.file.endswith((".xls", ".xlsx")):
            df = pd.read_excel(args.file)
        else:
            print(f"Error: Unsupported file format: {args.file}")
            print("Supported formats: .csv, .xls, .xlsx")
            return
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # Execute the command
    if args.command == "overview":
        overview.quick_look(df, name=args.name)

    elif args.command == "clean":
        # Clean the DataFrame
        if args.standardize:
            df = cleaning.update_col(df, standardize_col=True)

        # Save the cleaned DataFrame
        if args.output:
            if args.output.endswith(".csv"):
                df.to_csv(args.output, index=False)
            elif args.output.endswith((".xls", ".xlsx")):
                df.to_excel(args.output, index=False)
            else:
                print(f"Error: Unsupported output format: {args.output}")
                print("Supported formats: .csv, .xls, .xlsx")
                return

            print(f"Cleaned DataFrame saved to {args.output}")
        else:
            # Print the first few rows
            print("Cleaned DataFrame:")
            print(df.head())

    elif args.command == "report":
        # Generate the report
        result = report.generate_summary_report(
            df,
            title=args.title,
            include_plots=args.plots,
            output_format=args.format,
            output_path=args.output
        )

        # If output_path is None, print the report
        if args.output is None:
            print(result)


if __name__ == "__main__":
    main()
