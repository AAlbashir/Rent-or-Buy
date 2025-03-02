import unittest
import pandas as pd
from quality_of_life import load_data, compute_quality_of_life

class TestQualityOfLife(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load the Excel data once for all tests."""
        cls.file_path = "data/Random Cities in USA (Quality of Life Index).xlsx"
        cls.df = load_data(cls.file_path)

    def test_compute_quality_of_life_all_cities(self):
        """Test compute_quality_of_life for all cities in the dataset."""
        for city in self.df["City"].dropna():  # Ensure no NaN values in City column
            with self.subTest(city=city):
                try:
                    compute_quality_of_life(self.df, city)
                except Exception as e:
                    self.fail(f"compute_quality_of_life failed for {city}: {e}")

if __name__ == "__main__":
    unittest.main()
