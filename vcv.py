import pandas as pd
import matplotlib.pyplot as plt

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
    y1_col = df.loc[:, "Vacant housing units"] # Data for bar graph
    buy_line = df.loc[:, "Median Buy Cost (dollars)"]
    rent_line = df.loc[:, "Median Rent Cost (dollars)"]

    fig, ax1 = plt.subplots(figsize=(10, 10))
    plt.xticks(rotation=85)
    plt.xlabel("City")
    
    # Primary y-axis
    ax1.bar(x_col, y1_col, color='royalblue', label="Vacant housing units")
    ax1.set_ylabel("Number Vacant", color='black')
    ax1.legend(loc="upper left")
                  
    # Secondary y-axis
    ax2 = ax1.twinx()
    ax2.plot(x_col, buy_line, color='forestgreen', marker='o', linestyle='-', label="Median buy cost")
    ax2.plot(x_col, rent_line, color='darkred', marker='o', linestyle='-', label="Median rent cost")
    ax2.set_ylabel("Cost", color='black')
    ax2.legend(loc="best")

    fig.tight_layout()
    plt.show()

vacancy = "data/USA DP04 vacancy value cost.csv" 
plot_vacancy(vacancy)
