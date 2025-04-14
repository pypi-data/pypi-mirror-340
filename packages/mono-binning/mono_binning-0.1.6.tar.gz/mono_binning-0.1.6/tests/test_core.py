import unittest
import pandas as pd
import numpy as np
from mono_binning.core import mono_bin, char_bin, calculate_iv, calculate_rf_importance, calculate_iv_sequential, calculate_iv_parallel

class TestCore(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.df = pd.DataFrame({
            'target': [0, 1, 0, 1, 1, 0, 1, 0, 0, 1],
            'feature1': [1, 2, 2, 3, 4, 5, 6, 7, 8, 9],
            'feature2': ['A', 'B', 'A', 'B', 'B', 'A', 'A', 'B', 'B', 'A']
        })
        
        self.df_missing = pd.DataFrame({
            'target': [0, 1, 0, 1, 1, 0, 1, 0, 0, 1],
            'feature1': [1, 2, np.nan, 3, 4, 5, 6, np.nan, 8, 9],
            'feature2': ['A', 'B', 'A', 'B', 'B', 'A', 'A', 'B', 'B', 'A']
        })

    def test_mono_bin(self):
        # Test for numerical feature binning
        bin_stats, woe_map = mono_bin(self.df['target'], self.df['feature1'], n=5, alpha=0.5)
        self.assertGreater(len(bin_stats), 0)
        self.assertIn('WOE', bin_stats.columns)

    def test_char_bin(self):
        # Test for categorical feature binning
        bin_stats, woe_map = char_bin(self.df['target'], self.df['feature2'], alpha=0.5)
        self.assertGreater(len(bin_stats), 0)
        self.assertIn('WOE', bin_stats.columns)

    def test_calculate_iv_sequential(self):
        # Test for sequential IV calculation
        iv_summary, df_woe, woe_maps = calculate_iv_sequential(self.df, target='target', alpha=0.5)
        self.assertGreater(len(iv_summary), 0)
        self.assertIn('IV', iv_summary.columns)

    def test_calculate_iv_parallel(self):
        # Test for parallel IV calculation
        iv_summary, df_woe, woe_maps = calculate_iv_parallel(self.df, target='target', alpha=0.5, max_workers=2)
        self.assertGreater(len(iv_summary), 0)
        self.assertIn('IV', iv_summary.columns)

    def test_calculate_iv_invalid_target(self):
        # Test for invalid target column
        with self.assertRaises(ValueError):
            calculate_iv(self.df, target='invalid_target')

    def test_calculate_iv_insufficient_classes(self):
        # Test for target column with insufficient classes (only one unique value)
        df_single_class = pd.DataFrame({
            'target': [1, 1, 1, 1, 1],
            'feature1': [1, 2, 3, 4, 5]
        })
        with self.assertRaises(ValueError):
            calculate_iv(df_single_class, target='target')

    def test_calculate_rf_importance(self):
        # Test for random forest feature importance calculation
        importance_df = calculate_rf_importance(self.df, target='target', features=['feature1', 'feature2'])
        self.assertGreater(len(importance_df), 0)
        self.assertIn('Feature', importance_df.columns)
        self.assertIn('Importance', importance_df.columns)

    def test_calculate_rf_importance_missing(self):
        # Test for random forest feature importance with missing values
        importance_df = calculate_rf_importance(self.df_missing, target='target', features=['feature1', 'feature2'])
        self.assertGreater(len(importance_df), 0)
        self.assertIn('Feature', importance_df.columns)
        self.assertIn('Importance', importance_df.columns)

    def test_calculate_iv_invalid_execution_mode(self):
        # Test for invalid execution mode in IV calculation
        with self.assertRaises(ValueError):
            calculate_iv(self.df, target='target', execution='invalid_mode')

    def test_calculate_iv_concurrent(self):
        # Test for concurrent IV calculation
        iv_summary, df_woe, woe_maps = calculate_iv(self.df, target='target', alpha=0.5, execution="concurrent", max_workers=2)
        self.assertGreater(len(iv_summary), 0)
        self.assertIn('IV', iv_summary.columns)

if __name__ == '__main__':
    unittest.main()
