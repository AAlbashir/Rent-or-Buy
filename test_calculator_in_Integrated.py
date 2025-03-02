import unittest
from Rent_or_Buy_Integrated import compare_rent_vs_buy  # Import from Rent_or_Buy_Integrated

class TestCalculatorResult(unittest.TestCase):
   
    def test_rent_cheaper(self):
        """
        Test case where renting is cheaper than buying.
        """
        inputs = {
            "length_of_stay": 1,  # years
            "monthly_rent": 1,  # dollars
            "home_price": 117.70,  # dollars
            "down_payment": 0,  # dollars
            "mortgage_rate": 0,  # percent
            "investment_interest_rate": 0  # percent
        }
        result = compare_rent_vs_buy(**inputs)
        expected = {
            "Rent Cost": 12, 
            "Buy Cost": 12.01, 
            "Recommendation": 'Renting is financially better.'
        }
        self.assertEqual(result, expected)
    
    def test_buy_cheaper(self):
        """
        Test case where buying is cheaper than renting.
        """
        inputs = {
            "length_of_stay": 1,  # years
            "monthly_rent": 1,  # dollars
            "home_price": 117.59,  # dollars
            "down_payment": 0,  # dollars
            "mortgage_rate": 0,  # percent
            "investment_interest_rate": 0  # percent
        }
        result = compare_rent_vs_buy(**inputs)
        expected = {
            "Rent Cost": 12, 
            "Buy Cost": 11.99, 
            "Recommendation": 'Buying is financially better.'
        }
        self.assertEqual(result, expected)
   
    def test_equal_cost(self):
        """
        Test case where renting and buying costs are equal.
        """
        inputs = {
            "length_of_stay": 1,  # years
            "monthly_rent": 1,  # dollars
            "home_price": 117.65,  # dollars
            "down_payment": 0,  # dollars
            "mortgage_rate": 0,  # percent
            "investment_interest_rate": 0  # percent
        }
        result = compare_rent_vs_buy(**inputs)
        expected = {
            "Rent Cost": 12, 
            "Buy Cost": 12, 
            "Recommendation": 'Either.'
        }
        self.assertEqual(result, expected)

# Added Name-Main idiom to ensure that the test cases are executed only when the script is run directly and not when it is imported as a module
if __name__ == "__main__":
    unittest.main()
