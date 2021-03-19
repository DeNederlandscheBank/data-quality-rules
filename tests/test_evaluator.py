import unittest
import os
import data_patterns
import arelle
import pandas as pd
from src import Evaluator
from os.path import join, isfile  


class TestEval_patterns(unittest.TestCase):
    """Tests for `data_patterns` package."""

    def test_eval(self):
        """Test of read input date function"""
        # Input
        df_rules = pd.read_excel('tests/data/unittest_testset_aanvullende_regels.xlsx', engine='openpyxl', header = 1)
        df_rules.set_index('ControleRegelCode', inplace = True)

        # Expected output
        expected = pd.read_excel('tests/data/unittest_resulterende_patterns.xlsx', engine='openpyxl').fillna("")
        expected.set_index('index', inplace=True)

        # Actual output
        df_datapoints = pd.read_csv(join('data', 'datapoints', 'QRS.csv'), sep=';').fillna("")
        PARAMETERS = {'decimal':0}
        evaluator = Evaluator(df_rules, df_datapoints, PARAMETERS)
        actual = evaluator.df_patterns
        actual['encodings'] = actual['encodings'].astype(str)


        # Assert
        self.assertEqual(type(actual), type(expected), "Evaluator does not match")


        pd.testing.assert_frame_equal(actual, expected)
