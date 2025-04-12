# coding: utf-8
"""
DSHelperTool: A lightweight helper package for data science and analysis tasks.
"""

__version__ = "0.1.0"

from . import overview
from . import cleaning
from . import dtypes
from . import eda
from . import stats
from . import viz
from . import report
from . import easter_egg

# Import commonly used functions for easier access
from .overview import quick_look, get_duplicates, value_counts_all
from .cleaning import update_col, drop_cols
from .dtypes import to_numeric_cols, to_datetime_cols
from .eda import check_skew, plot_skew, fill_missing
from .stats import describe_all, group_stats, outlier_detection, hypothesis_test, correlation_matrix
from .viz import plot_missing, plot_distributions, plot_categorical, plot_correlation, plot_boxplots, plot_scatter_matrix, plot_time_series, plot_group_comparison
from .report import generate_summary_report, export_to_excel, generate_data_dictionary
from .easter_egg import fortune_cookie
