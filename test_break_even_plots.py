import unittest
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Prevents plots from appearing during tests
import matplotlib.pyplot as plt
from unittest.mock import patch
from Break_even_Plots import plot_sensitivity_analysis

class TestPlotSensitivityAnalysis(unittest.TestCase):

    def setUp(self):
        """ Set up valid base inputs for tests """
        self.valid_inputs = {
            "length_of_stay": 5,
            "monthly_rent": 2000,
            "home_price": 500000,
            "down_payment": 100000,
            "mortgage_rate": 5.0,
            "investment_interest_rate": 4.0
        }

    @patch("matplotlib.pyplot.show")
    def test_factors_not_multiple_of_increment(self, mock_show):
        """ Test for factors that are not multiples of the increments defined """
        # Test each factor with a value that is not a multiple of the increment
        test_cases = {
            "length_of_stay": 2.5,  # Not a multiple of 1 (increment is 1)
            "monthly_rent": 1050,  # Not a multiple of 100 (increment is 100)
            "home_price": 100500,  # Not a multiple of 1000 (increment is 1000)
            "down_payment": 1500,  # Not a multiple of 1000 (increment is 1000)
            "mortgage_rate": 5.25,  # Not a multiple of 0.5 (increment is 0.5)
            "investment_interest_rate": 4.05  # Not a multiple of 0.1 (increment is 0.1)
        }
        
        for factor, value in test_cases.items():
            with self.subTest(factor=factor):
                test_inputs = self.valid_inputs.copy()
                test_inputs[factor] = value

                try:
                    plot_sensitivity_analysis(test_inputs)
                except Exception as e:
                    self.assertTrue(False, f"plot_sensitivity_analysis failed with non-multiple value for {factor}: {e}")
                
                # Close the figure after plotting to prevent memory overload
                plt.close()

    @patch("matplotlib.pyplot.show")
    def test_factors_at_zero(self, mock_show):
        """ Test for factors that are set to zero """
        # Test each factor with a zero value
        test_cases = {
            "length_of_stay": 0,  # Zero value
            "monthly_rent": 0,  # Zero value
            "home_price": 0,  # Zero value
            "down_payment": 0,  # Zero value
            "mortgage_rate": 0,  # Zero value
            "investment_interest_rate": 0  # Zero value
        }

        for factor, value in test_cases.items():
            with self.subTest(factor=factor):
                test_inputs = self.valid_inputs.copy()
                test_inputs[factor] = value

                try:
                    plot_sensitivity_analysis(test_inputs)
                except Exception as e:
                    self.assertTrue(False, f"plot_sensitivity_analysis failed with zero value for {factor}: {e}")
                
                # Close the figure after plotting to prevent memory overload
                plt.close()

    @patch("matplotlib.pyplot.show")
    def test_negative_factors(self, mock_show):
        """ Test for factors that are negative values """
        # Test each factor with a negative value
        test_cases = {
            "length_of_stay": -1,  # Negative value
            "monthly_rent": -500,  # Negative value
            "home_price": -100000,  # Negative value
            "down_payment": -5000,  # Negative value
            "mortgage_rate": -0.5,  # Negative value
            "investment_interest_rate": -1.5  # Negative value
        }

        for factor, value in test_cases.items():
            with self.subTest(factor=factor):
                test_inputs = self.valid_inputs.copy()
                test_inputs[factor] = value

                try:
                    plot_sensitivity_analysis(test_inputs)
                except Exception as e:
                    self.assertTrue(False, f"plot_sensitivity_analysis failed with negative value for {factor}: {e}")
                
                # Close the figure after plotting to prevent memory overload
                plt.close()

if __name__ == '__main__':
    unittest.main()

