import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

def plot_vacancy(vacancy):
    """
    Plots number of vacant homes, median home value, and median costs to rent and buy for selected cities.
    """
       
    df = pd.read_csv(vacancy)

    # Convert numerical columns from object to integer
    cols_to_convert = ["Vacant housing units", "Median House Value (dollars)", "Median Buy Cost (dollars)", "Median Rent Cost (dollars)"]

    for col in cols_to_convert:
        df[col] = df[col].str.replace(",", "").astype(int)

    # Remove "!!Estimate" from city names
    df["City"] = df["City"].str.replace("!!Estimate", "").str.strip()
     
    x_col = df.loc[:, "City"] # x-axis values
    y1_col = df.loc[:, "Vacant housing units"] # Data for bar chart 1
    y2_col = df.loc[:, "Median House Value (dollars)"] # Data for bar chart 2
    buy_line = df.loc[:, "Median Buy Cost (dollars)"]
    rent_line = df.loc[:, "Median Rent Cost (dollars)"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 5))
    
                           
    # Primary y-axis - chart 1
    ax1.bar(x_col, y1_col, color='slategrey', label="Vacant housing units")
    ax1.set_xlabel("City", fontsize=14)
    ax1.set_xticks(ax1.get_xticks())
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=85, ha='right')
    # ax1.set_xticklabels(x_col, rotation=85)
    ax1.set_ylabel("Number Vacant", color='black')
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f"{int(x/1000)}K"))
    ax1.legend(loc="upper left")
    
                  
    # Secondary y-axis - chart 1
    secax_ax1 = ax1.twinx()
    secax_ax1.plot(x_col, buy_line, color='forestgreen', marker='o', linestyle='-', label="Median buy cost")
    secax_ax1.plot(x_col, rent_line, color='darkred', marker='o', linestyle='-', label="Median rent cost")
    secax_ax1.set_ylabel("Cost (USD)", color='black')
    secax_ax1.legend(loc="best")

    # Chart 1
    plt.title("Vacancy & Cost", fontsize=14, fontweight="bold")
    
    # Primary y-axis - chart 2
    ax2.bar(x_col, y2_col, color='tan', label="Median home value")
    ax2.set_xlabel("City", fontsize=14)
    ax2.set_xticks(ax2.get_xticks())
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=85, ha='right')
    # ax2.set_xticklabels(x_col, rotation=85)
    ax2.set_ylabel("Home Value (USD)", color='black')
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f"{int(x/1000)}K"))    
    ax2.legend(loc="upper left")
    
                  
    # Secondary y-axis - chart 2
    secax_ax2 = ax2.twinx()
    secax_ax2.plot(x_col, buy_line, color='forestgreen', marker='o', linestyle='-', label="Median buy cost")
    secax_ax2.plot(x_col, rent_line, color='darkred', marker='o', linestyle='-', label="Median rent cost")
    secax_ax2.set_ylabel("Cost (USD)", color='black')
    secax_ax2.legend(loc="best")

    # Chart 2
    plt.title("Home Value & Cost", fontsize=14, fontweight="bold")
    
    plt.show()

vacancy = "data/USA DP04 vacancy value cost.csv" 
plot_vacancy(vacancy)
