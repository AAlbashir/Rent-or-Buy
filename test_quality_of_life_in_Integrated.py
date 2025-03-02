import unittest
import pandas as pd
from Rent_or_Buy_Integrated import compute_quality_of_life  # Import from Rent_or_Buy_Integrated instead of Quality_of_Life

class TestQualityOfLife(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load the Excel data once for all tests."""
        cls.file_path = "data/Random Cities in USA (Rent & Buy).xlsx"
        cls.df = pd.read_excel(cls.file_path)  # Use pd.read_excel directly since load_data is not in Rent_or_Buy_Integrated

    def test_compute_quality_of_life_all_cities(self):
        """Test compute_quality_of_life for each city in the dataset only once."""
        # Get unique city names by dropping duplicates
        unique_cities = self.df["City"].drop_duplicates().dropna()  # Ensure no NaN values in City column

        for city in unique_cities:  # Iterate over unique cities
            with self.subTest(city=city):
                try:
                    compute_quality_of_life(self.df, city)  # Call the function from Rent_or_Buy_Integrated
                except Exception as e:
                    self.fail(f"compute_quality_of_life failed for {city}: {e}")

if __name__ == "__main__":
    unittest.main()
