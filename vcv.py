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

    # Chart 1
    fig, ax1 = plt.subplots(figsize=(10, 5))
    plt.title("Vacancy & Cost")
    plt.xticks(rotation=85)
    plt.xlabel("City")
        
    # Primary y-axis - chart 1
    ax1.bar(x_col, y1_col, color='slategrey', label="Vacant housing units")
    ax1.set_ylabel("Number Vacant", color='black')
    ax1.legend(loc="upper left")
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f"{int(x/1000)}K"))
                  
    # Secondary y-axis - chart 1
    ax2 = ax1.twinx()
    ax2.plot(x_col, buy_line, color='forestgreen', marker='o', linestyle='-', label="Median buy cost")
    ax2.plot(x_col, rent_line, color='darkred', marker='o', linestyle='-', label="Median rent cost")
    ax2.set_ylabel("Cost (USD)", color='black')
    ax2.legend(loc="best")

    # Chart 2
    fig, ax3 = plt.subplots(figsize=(10, 5))
    plt.title("Home Value & Cost")
    plt.xticks(rotation=85)
    plt.xlabel("City")
    
    # Primary y-axis - chart 2
    ax3.bar(x_col, y2_col, color='royalblue', label="Median home value")
    ax3.set_ylabel("Home Value (USD)", color='black')
    ax3.legend(loc="upper left")
    ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f"{int(x/1000)}K"))
                  
    # Secondary y-axis - chart 2
    ax4 = ax3.twinx()
    ax4.plot(x_col, buy_line, color='forestgreen', marker='o', linestyle='-', label="Median buy cost")
    ax4.plot(x_col, rent_line, color='darkred', marker='o', linestyle='-', label="Median rent cost")
    ax4.set_ylabel("Cost (USD)", color='black')
    ax4.legend(loc="best")

    plt.show()

vacancy = "data/USA DP04 vacancy value cost.csv" 
plot_vacancy(vacancy)
