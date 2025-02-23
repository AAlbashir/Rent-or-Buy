import unittest
import numpy as np
import matplotlib.pyplot as plt
from break_even_plots import plot_sensitivity_analysis

class TestPlotSensitivityAnalysis(unittest.TestCase):

    def setUp(self):
        """ Set up valid base inputs for tests """
        self.valid_inputs = {
            "length_of_stay": 5,  # Years planning to stay in the home
            "monthly_rent": 2000,  # Monthly rent cost in dollars
            "home_price": 500000,  # Purchase price of the home in dollars
            "down_payment": 100000,  # Initial down payment amount in dollars
            "mortgage_rate": 5.0,  # Annual mortgage interest rate (percentage)
            "investment_interest_rate": 4.0  # Annual investment interest rate (percentage)            
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
            "length_of_stay": 2.5, # Not mutliple of 1 increment defined
            "monthly_rent": 1050, # Not mutliple of 100 increment defined
            "home_price": 100500, # Not mutliple of 1000 increment defined
            "down_payment": 1500, # Not mutliple of 1000 increment defined
            "mortgage_rate": 5.25, # Not mutliple of 0.5 increment defined
            "investment_interest_rate": 4.05 # Not mutliple of 0.5 increment defined
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
            "length_of_stay": 0.01,  # Near-zero stay duration
            "monthly_rent": 0.1,  # Extremely low rent
            "home_price": 1,  # Unrealistically low home price
            "down_payment": 0.01,  # Tiny down payment
            "mortgage_rate": 0.001,  # Very low mortgage rate
            "investment_interest_rate": 0.0001  # Almost zero investment return
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
            "length_of_stay": 1000,  # Extremely long stay duration
            "monthly_rent": 1e7,  # Very high rent
            "home_price": 1e9,  # Very high home price
            "down_payment": 1e8,  # Huge down payment
            "mortgage_rate": 99.9,  # Unrealistically high mortgage rate
            "investment_interest_rate": 100.0  # Very high investment return rate
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
