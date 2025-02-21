import unittest
import numpy as np
import matplotlib.pyplot as plt
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

    def test_valid_inputs(self):
        """ Test for valid inputs to ensure plotting works """
        try:
            plot_sensitivity_analysis(self.valid_inputs)
        except Exception as e:
            self.assertTrue(False, f"plot_sensitivity_analysis failed with valid inputs: {e}")
        
        plt.close()  # Close figure after plotting

    def test_factors_not_multiple_of_increment(self):
        """ Test for factors that are not multiples of the increments defined """
        test_cases = {
            "length_of_stay": 2.5,
            "monthly_rent": 1050,
            "home_price": 100500,
            "down_payment": 1500,
            "mortgage_rate": 5.25,
            "investment_interest_rate": 4.05
        }

        for factor, value in test_cases.items():
            with self.subTest(factor=factor):
                test_inputs = self.valid_inputs.copy()
                test_inputs[factor] = value

                try:
                    plot_sensitivity_analysis(test_inputs)
                except Exception as e:
                    self.assertTrue(False, f"plot_sensitivity_analysis failed for {factor}: {e}")

                plt.close()

    def test_very_small_values(self):
        """ Test for very small positive values near zero """
        test_cases = {
            "length_of_stay": 0.01,
            "monthly_rent": 0.1,
            "home_price": 1,
            "down_payment": 0.01,
            "mortgage_rate": 0.001,
            "investment_interest_rate": 0.0001
        }

        for factor, value in test_cases.items():
            with self.subTest(factor=factor):
                test_inputs = self.valid_inputs.copy()
                test_inputs[factor] = value

                try:
                    plot_sensitivity_analysis(test_inputs)
                except Exception as e:
                    self.assertTrue(False, f"plot_sensitivity_analysis failed for very small {factor}: {e}")

                plt.close()

    def test_very_large_values(self):
        """ Test for very large values """
        test_cases = {
            "length_of_stay": 1000,
            "monthly_rent": 1e7,
            "home_price": 1e9,
            "down_payment": 1e8,
            "mortgage_rate": 99.9,
            "investment_interest_rate": 100.0
        }

        for factor, value in test_cases.items():
            with self.subTest(factor=factor):
                test_inputs = self.valid_inputs.copy()
                test_inputs[factor] = value

                try:
                    plot_sensitivity_analysis(test_inputs)
                except Exception as e:
                    self.assertTrue(False, f"plot_sensitivity_analysis failed for very large {factor}: {e}")

                plt.close()

if __name__ == '__main__':
    unittest.main()
