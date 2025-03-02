import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Load the Excel file
file_path = 'data/Random Cities in USA (Rent & Buy).xlsx'
df = pd.read_excel(file_path)

# Function to get user inputs and filter the data
def get_user_inputs():
    # Get available cities
    available_cities = df['City'].unique()
    print("Available cities:", ", ".join(available_cities))
    city = input("Enter the city: ").strip()
    
    # Get location
    location = input("Enter location (City Centre or Outside City Centre): ").strip()
    
    # Get number of bedrooms
    bedrooms = input("Enter number of bedrooms (1 or 3): ").strip()
    
    # Filter the data based on user inputs
    filtered_data = df[(df['City'] == city) & 
                       (df['Location'] == location) & 
                       (df['Number of Bedrooms'] == int(bedrooms))]
    
    if filtered_data.empty:
        print("No data found for the given inputs. Please try again.")
        return get_user_inputs()
    
    # Extract values from the filtered data
    monthly_rent = filtered_data['Rent per Month'].values[0]
    home_price = filtered_data['Buy Apartment Price Total'].values[0]
    mortgage_rate = filtered_data['Mortgage Intrest Rate'].values[0]
    
    # Get additional inputs
    length_of_stay = float(input("Enter length of stay in years: "))
    down_payment = float(input("Enter down payment in dollars: "))
    investment_interest_rate = float(input("Enter investment interest rate (as percentage): "))
    
    return {
        "length_of_stay": length_of_stay,
        "monthly_rent": monthly_rent,
        "home_price": home_price,
        "down_payment": down_payment,
        "mortgage_rate": mortgage_rate,
        "investment_interest_rate": investment_interest_rate,
        "city": city  # Return the city for quality of life calculation
    }

# Function to compare renting vs buying
def compare_rent_vs_buy(length_of_stay, monthly_rent, home_price, down_payment, mortgage_rate, investment_interest_rate, property_tax_rate=1.2, maintenance_rate=1.0, selling_cost_rate=8.0): 
    """
    Compare renting vs. buying a home.
    
    :param length_of_stay: Years planning to stay in the home
    :param monthly_rent: Monthly rent cost
    :param home_price: Purchase price of the home
    :param down_payment: Initial down payment amount
    :param mortgage_rate: Annual mortgage interest rate (as percentage)
    :param property_tax_rate: Annual property tax rate (default 1.2%)
    :param maintenance_rate: Annual maintenance cost rate (default 1.0%)
    :param investment_interest_rate: Annual investment interest (as percentage)
    :param selling_cost_rate: Cumulative costs of selling a home (default 8.0%)
    :return: Total costs for renting and buying, and recommendation
    """
          
    # Renting cost calculations
    investment = (down_payment * (investment_interest_rate / 100)) * length_of_stay 
    total_rent_cost = (monthly_rent * 12 * length_of_stay) - investment
    final_rent_cost = round(total_rent_cost, 2) #Rounded cost to account for real currency values

    
    # Buying cost calculations
    loan_amount = home_price - down_payment
    monthly_interest_rate = (mortgage_rate / 100) / 12
    num_payments = length_of_stay * 12
    home_appreciation = home_price * (1 + (investment_interest_rate / 100) / 12)**(12 * length_of_stay) 
    selling_costs = home_appreciation * (selling_cost_rate / 100) 

    
    if monthly_interest_rate > 0:
        monthly_mortgage_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** num_payments) / ((1 + monthly_interest_rate) ** num_payments - 1)
    else:
        monthly_mortgage_payment = loan_amount / num_payments
    
    total_mortgage_cost = monthly_mortgage_payment * num_payments
    total_property_tax = (property_tax_rate / 100) * home_price * length_of_stay
    total_maintenance = (maintenance_rate / 100) * home_price * length_of_stay
    total_resale_value = home_appreciation - selling_costs 

    total_buy_cost = down_payment + total_mortgage_cost + total_property_tax + total_maintenance - total_resale_value
    final_buy_cost = round(total_buy_cost, 2) #Rounded cost to account for real currency values
    
    # Recommendation
    if final_rent_cost < final_buy_cost:
        recommendation = "Renting is financially better."
    elif final_rent_cost > final_buy_cost:
        recommendation = "Buying is financially better."
    else:
        recommendation = "Either."
    
    return {
        "Rent Cost": final_rent_cost,
        "Buy Cost": final_buy_cost,
        "Recommendation": recommendation
    }

# Function to plot sensitivity analysis
def plot_sensitivity_analysis(base_inputs):
    """
    Plots how the total rent and buy costs change when varying one input factor at a time.
    """
    # Define the factors to be varied along with their start, stop, and increment values
    factors = {
        "length_of_stay": (1, base_inputs["length_of_stay"], 1),
        "monthly_rent": (0, base_inputs["monthly_rent"], 100),
        "home_price": (0, base_inputs["home_price"], 1000),
        "down_payment": (0, base_inputs["down_payment"], 1000),
        "mortgage_rate": (0, base_inputs["mortgage_rate"], 0.5),
        "investment_interest_rate": (0, base_inputs["investment_interest_rate"], 0.5)
    }
    
    # Iterate over each factor to analyze its impact
    for factor, (start, stop, step) in factors.items():
        values = np.arange(start, stop + step, step)
        rent_costs, buy_costs = [], []
        
        # Compute rent and buy costs for each value of the current factor
        for value in values:
            inputs = base_inputs.copy()
            inputs[factor] = value
            result = compare_rent_vs_buy(**inputs)
            rent_costs.append(result["Rent Cost"])
            buy_costs.append(result["Buy Cost"])
        
        # Generate the plot for the current factor
        plt.figure(figsize=(8, 5))
        plt.plot(values, rent_costs, label='Rent Cost', marker='o')
        plt.plot(values, buy_costs, label='Buy Cost', marker='s')
        plt.xlabel(factor.replace("_", " ").title())
        plt.ylabel("Cost (USD)")
        plt.title(f"Impact of {factor.replace('_', ' ').title()} on Rent vs. Buy Cost")
        plt.legend()
        plt.grid()
        plt.show()

# Function to plot vacancy and cost data
def plot_vacancy(excel_file):
    """
    Plots number of vacant homes, median home value, and median costs to rent and buy for selected cities.
    """
       
    # Read the Excel file
    df = pd.read_excel(excel_file)

    # Group data by city and calculate the mean for relevant columns
    grouped_df = df.groupby('City').agg({
        'Vacant housing units': 'mean',  # Use mean to aggregate
        'Median House Value (dollars)': 'mean',
        'Median Buy Cost (dollars)': 'mean',
        'Median Rent Cost (dollars)': 'mean'
    }).reset_index()

    # Convert numerical columns to integer (if necessary)
    cols_to_convert = ["Vacant housing units", "Median House Value (dollars)", "Median Buy Cost (dollars)", "Median Rent Cost (dollars)"]
    for col in cols_to_convert:
        grouped_df[col] = grouped_df[col].astype(int)

    # x-axis values (city names)
    x_col = grouped_df.loc[:, "City"]
    
    # Data for bar chart 1 (vacant housing units)
    y1_col = grouped_df.loc[:, "Vacant housing units"]
    
    # Data for bar chart 2 (median house value)
    y2_col = grouped_df.loc[:, "Median House Value (dollars)"]
    
    # Data for lines (median buy and rent costs)
    buy_line = grouped_df.loc[:, "Median Buy Cost (dollars)"]
    rent_line = grouped_df.loc[:, "Median Rent Cost (dollars)"]

    # Create subplots
    fig, ax = plt.subplots(1, 2, figsize=(20, 5))
                   
    # Primary y-axis - chart 1 (vacant housing units)
    ax[0].bar(x_col, y1_col, color='slategrey', label="Vacant housing units")
    ax[0].set_xlabel("City", fontsize=14)
    
    # Set x-ticks and labels for chart 1
    ax[0].set_xticks(range(len(x_col)))  # Set ticks at positions 0, 1, 2, etc.
    ax[0].set_xticklabels(x_col, rotation=85)  # Set labels and rotate them
    
    ax[0].set_ylabel("Number Vacant", color='black')
    ax[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f"{int(x/1000)}K"))
    ax[0].legend(loc="upper left")
    
    # Secondary y-axis - chart 1 (median buy and rent costs)
    ax2 = ax[0].twinx()
    ax2.plot(x_col, buy_line, color='forestgreen', marker='o', linestyle='-', label="Median buy cost")
    ax2.plot(x_col, rent_line, color='darkred', marker='o', linestyle='-', label="Median rent cost")
    ax2.set_ylabel("Cost (USD)", color='black')
    ax2.legend(loc="best")

    # Chart 1 title
    ax[0].set_title("Vacancy & Cost", fontsize=14, fontweight="bold")
    
    # Primary y-axis - chart 2 (median home value)
    ax[1].bar(x_col, y2_col, color='tan', label="Median home value")
    ax[1].set_xlabel("City", fontsize=14)
    
    # Set x-ticks and labels for chart 2
    ax[1].set_xticks(range(len(x_col)))  # Set ticks at positions 0, 1, 2, etc.
    ax[1].set_xticklabels(x_col, rotation=85)  # Set labels and rotate them
    
    ax[1].set_ylabel("Home Value (USD)", color='black')
    ax[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f"{int(x/1000)}K"))    
    ax[1].legend(loc="upper left")
    
    # Secondary y-axis - chart 2 (median buy and rent costs)
    ax4 = ax[1].twinx()
    ax4.plot(x_col, buy_line, color='forestgreen', marker='o', linestyle='-', label="Median buy cost")
    ax4.plot(x_col, rent_line, color='darkred', marker='o', linestyle='-', label="Median rent cost")
    ax4.set_ylabel("Cost (USD)", color='black')
    ax4.legend(loc="best")

    # Chart 2 title
    ax[1].set_title("Home Value & Cost", fontsize=14, fontweight="bold")
    
    # Show the plots
    plt.tight_layout()
    plt.show()

# Function to compute Quality of Life Index
def compute_quality_of_life(data, city):
    """Compute the Quality of Life Index for a given city."""
    row = data[data['City'] == city]
    if row.empty:
        print("City not found.")
        return
    
    # Print the city name before categorized values
    print(f"City: {city}")
    
    # Extract values and convert to float where possible
    try:
        pp = float(row["Purchasing Power Index"].values[0])
        safety = float(row["Safety Index"].values[0])
        health = float(row["Health Care Index"].values[0])
        climate = float(row["Climate Index"].values[0])
        col = float(row["Cost Of Living Index"].values[0])
        prop = float(row["Property Price to Income Ratio"].values[0])
        traffic = float(row["Traffic Commute Time Index"].values[0])
        pollution = float(row["Pollution Index"].values[0])
    except:
        print("Missing value in data.")
        return
    
    # Compute Quality of Life Index
    qol = max(0, 100 + pp / 2.5 - prop * 1.0 - col / 10 + safety / 2.0 + health / 2.5 - traffic / 2.0 - pollution * 2.0 / 3.0 + climate / 3.0)
    
    # Define thresholds and labels
    thresholds = {
        "Purchasing Power Index": [40, 80, 120, 160],
        "Safety Index": [20, 40, 60, 80],
        "Health Care Index": [20, 40, 60, 80],
        "Climate Index": [20, 40, 60, 80],
        "Cost Of Living Index": [20, 40, 60, 80],
        "Property Price to Income Ratio": [2, 4, 6, 8],
        "Traffic Commute Time Index": [20, 40, 60, 80],
        "Pollution Index": [20, 40, 60, 80],
        "Quality of Life Index": [48, 96, 144, 192]
    }
    
    labels = ["Very Low", "Low", "Moderate", "High", "Very High"]
    
    # Print categorized values
    print(f"Purchasing Power Index: {pp} ({categorize_value(pp, thresholds['Purchasing Power Index'], labels)})")
    print(f"Safety Index: {safety} ({categorize_value(safety, thresholds['Safety Index'], labels)})")
    print(f"Health Care Index: {health} ({categorize_value(health, thresholds['Health Care Index'], labels)})")
    print(f"Climate Index: {climate} ({categorize_value(climate, thresholds['Climate Index'], labels)})")
    print(f"Cost Of Living Index: {col} ({categorize_value(col, thresholds['Cost Of Living Index'], labels)})")
    print(f"Property Price to Income Ratio: {prop} ({categorize_value(prop, thresholds['Property Price to Income Ratio'], labels)})")
    print(f"Traffic Commute Time Index: {traffic} ({categorize_value(traffic, thresholds['Traffic Commute Time Index'], labels)})")
    print(f"Pollution Index: {pollution} ({categorize_value(pollution, thresholds['Pollution Index'], labels)})")
    print(f"Quality of Life Index: {qol} ({categorize_value(qol, thresholds['Quality of Life Index'], labels)})")

# Function to categorize values
def categorize_value(value, thresholds, labels):
    """Categorize a numerical value based on given thresholds."""
    for i, threshold in enumerate(thresholds):
        if value <= threshold:
            return labels[i]
    return labels[-1]

# Main execution
if __name__ == "__main__":
    # Get user inputs for rent vs buy comparison
    inputs = get_user_inputs()

    # Remove the 'city' key from inputs before passing to compare_rent_vs_buy
    city = inputs.pop("city")  # Remove and store the city for later use

    # Compare rent vs buy
    result = compare_rent_vs_buy(**inputs)
    print(result)

    # Plot sensitivity analysis
    plot_sensitivity_analysis(inputs)

    # Plot vacancy and cost data
    plot_vacancy(file_path)

    # Compute and print Quality of Life Index for the selected city
    compute_quality_of_life(df, city)
