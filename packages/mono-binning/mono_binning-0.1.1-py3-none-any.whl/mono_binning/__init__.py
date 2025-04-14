"""
mono_binning - Monotonic binning with IV/WOE transformation
"""

# src/mono_binning/__init__.py
# from .core import (
#     calculate_iv,
#     woe_iv_report,
#     woe_transform,
#     auto_bin,
#     char_bin,  # Categorical binning function
#     feature_importance,
#     mono_bin,
#     mono_bin_parallel,
#     char_bin_parallel
# )


# __init__.py
from .core import (
    calculate_iv,
    calculate_iv_parallel,
    calculate_iv_sequential,  # Using sequential instead of serial
    mono_bin,
    char_bin,
    _iv_worker,
    calculate_rf_importance
)

__all__ = [
    'calculate_iv',
    'calculate_iv_parallel',
    'calculate_iv_sequential',  # Corrected import
    'mono_bin',
    'char_bin',
    '_iv_worker',
    'calculate_rf_importance'
]

__version__ = '0.1.0'


