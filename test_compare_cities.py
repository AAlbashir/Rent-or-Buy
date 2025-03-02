import unittest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from unittest.mock import MagicMock, patch
import compare_cities

class TestCompareCities(unittest.TestCase):    
    vacancy = "data/USA DP04 vacancy value cost.csv"

    
    def test_chart_labels(self):
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1.set_xlabel("X Axis Label")
        ax1.set_ylabel("Left Y Axis")
        ax2.set_ylabel("Right Y Axis")

        assert ax1.get_xlabel() == "X Axis Label"
        assert ax1.get_ylabel() == "Left Y Axis"
        assert ax2.get_ylabel() == "Right Y Axis"
        
        
    def test_data_frame(self):  
        df = pd.read_csv("data/test_file.csv")
               
        # Convert numerical columns from object to integer
        cols_to_convert = ["y1", "y2"]    
        for col in cols_to_convert:
            df[col] = df[col].str.replace(",", "").astype(np.int64)

        expected_df = pd.DataFrame({"x": ["A", "B", "C", "D"], "y1": [100000, 200000, 300000, 400000], "y2": [1000, 2000, 3000, 4000]})
        
        pd.testing.assert_frame_equal(df, expected_df)
        

    def test_plot_function(self): 

                
        with patch("matplotlib.pyplot.subplots") as mock_subplots:
            mock_fig = MagicMock()
            mock_ax1 = MagicMock()
            mock_secax_ax1 = MagicMock()
            mock_ax2 = MagicMock()
            mock_secax_ax2 = MagicMock()
            
            mock_subplots.return_value = (mock_fig, (mock_ax1, mock_ax2))
            mock_ax1.twinx.return_value = mock_secax_ax1
            mock_ax2.twinx.return_value = mock_secax_ax2
                       
            compare_cities.plot_vacancy(self.vacancy)
                             
            mock_subplots.assert_called_once()
            mock_ax1.bar.assert_called_once() 
            mock_ax2.bar.assert_called_once()
            mock_secax_ax1.plot.assert_called()            
            mock_secax_ax2.plot.assert_called()
            mock_ax1.set_xlabel.assert_called_once()
            mock_ax1.set_ylabel.assert_called_once()
            mock_ax2.set_xlabel.assert_called_once()
            mock_ax2.set_ylabel.assert_called_once()
            mock_secax_ax1.set_ylabel.assert_called()
            mock_secax_ax2.set_ylabel.assert_called()
            
 
# Added Name-Main idiom to run unit test as a script and automatically load unittest module
if __name__== "__main__":
    unittest.main()