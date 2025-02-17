import Calculator
import unittest

class TestCalculatorResult(unittest.TestCase):
    """
    def setUp(self):
        self.result = Result('The result')
    """
    
    def test_rent_cheaper(self):
        inputs = {
            "length_of_stay": 1,  # years
            "monthly_rent": 1,  # dollars
            "home_price": 117.70,  # dollars
            "down_payment": 0,  # dollars
            "mortgage_rate": 0,  # percent
            "investment_interest_rate": 0 # percent
        }
        result = Calculator.compare_rent_vs_buy(**inputs)
        expected = {
            "Rent Cost": 12, 
            "Buy Cost": 12.01, 
            "Recommendation": 'Renting is financially better.'
        }
        self.assertEqual(result, expected)
    
    def test_buy_cheaper(self):
        inputs = {
            "length_of_stay": 1,  # years
            "monthly_rent": 1,  # dollars
            "home_price": 117.59,  # dollars
            "down_payment": 0,  # dollars
            "mortgage_rate": 0,  # percent
            "investment_interest_rate": 0 # percent
        }
        result = Calculator.compare_rent_vs_buy(**inputs)
        expected = {
            "Rent Cost": 12, 
            "Buy Cost": 11.99, 
            "Recommendation": 'Buying is financially better.'
        }
        self.assertEqual(result, expected)
   
    def test_2_compare_rent_vs_buy(self):
      inputs = {
            "length_of_stay": 1,  # years
            "monthly_rent": 1,  # dollars
            "home_price": 117.65,  # dollars
            "down_payment": 0,  # dollars
            "mortgage_rate": 0,  # percent
            "investment_interest_rate": 0 # percent
      }
      result = Calculator.compare_rent_vs_buy(**inputs)
      expected = {
            "Rent Cost": 12, 
            "Buy Cost": 12, 
            "Recommendation": 'Either.'
      }
      self.assertEqual(result, expected)