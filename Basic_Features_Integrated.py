import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

def compare_rent_vs_buy(length_of_stay, monthly_rent, home_price, down_payment, mortgage_rate, investment_interest_rate, property_tax_rate=1.2, maintenance_rate=1.0, selling_cost_rate=8.0):
    """
    Compare renting vs. buying a home.
    """
    investment = (down_payment * (investment_interest_rate / 100)) * length_of_stay 
    total_rent_cost = (monthly_rent * 12 * length_of_stay) - investment
    final_rent_cost = round(total_rent_cost, 2)
    
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
    final_buy_cost = round(total_buy_cost, 2)
    
    recommendation = "Renting is financially better." if final_rent_cost < final_buy_cost else "Buying is financially better." if final_rent_cost > final_buy_cost else "Either."
    
    return {"Rent Cost": final_rent_cost, "Buy Cost": final_buy_cost, "Recommendation": recommendation}

def plot_sensitivity_analysis(base_inputs):
    """
    Plots how the total rent and buy costs change when varying one input factor at a time.
    """
    factors = {
        "length_of_stay": (1, base_inputs["length_of_stay"], 1),
        "monthly_rent": (0, base_inputs["monthly_rent"], 100),
        "home_price": (0, base_inputs["home_price"], 1000),
        "down_payment": (0, base_inputs["down_payment"], 1000),
        "mortgage_rate": (0, base_inputs["mortgage_rate"], 0.5),
        "investment_interest_rate": (0, base_inputs["investment_interest_rate"], 0.5)
    }
    
    for factor, (start, stop, step) in factors.items():
        values = np.arange(start, stop + step, step)
        rent_costs, buy_costs = [], []
        
        for value in values:
            inputs = base_inputs.copy()
            inputs[factor] = value
            result = compare_rent_vs_buy(**inputs)
            rent_costs.append(result["Rent Cost"])
            buy_costs.append(result["Buy Cost"])
        
        plt.figure(figsize=(8, 5))
        plt.plot(values, rent_costs, label='Rent Cost', marker='o')
        plt.plot(values, buy_costs, label='Buy Cost', marker='s')
        plt.xlabel(factor.replace("_", " ").title())
        plt.ylabel("Cost (USD)")
        plt.title(f"Impact of {factor.replace('_', ' ').title()} on Rent vs. Buy Cost")
        plt.legend()
        plt.grid()
        plt.show()

def plot_vacancy(vacancy_file):
    """
    Plots number of vacant homes, median home value, and median costs to rent and buy for selected cities.
    """
    df = pd.read_csv(vacancy_file)
    cols_to_convert = ["Vacant housing units", "Median House Value (dollars)", "Median Buy Cost (dollars)", "Median Rent Cost (dollars)"]
    
    for col in cols_to_convert:
        df[col] = df[col].str.replace(",", "").astype(int)
    
    df["City"] = df["City"].str.replace("!!Estimate", "").str.strip()
    
    x_col, y1_col, y2_col = df["City"], df["Vacant housing units"], df["Median House Value (dollars)"]
    buy_line, rent_line = df["Median Buy Cost (dollars)"], df["Median Rent Cost (dollars)"]
    
    fig, ax = plt.subplots(1, 2, figsize=(20, 5))
    ax[0].bar(x_col, y1_col, color='slategrey', label="Vacant housing units")
    ax[0].set_xlabel("City", fontsize=14)
    ax[0].set_xticklabels(x_col, rotation=85)
    ax[0].set_ylabel("Number Vacant", color='black')
    ax[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f"{int(x/1000)}K"))
    ax[0].legend(loc="upper left")
    
    ax2 = ax[0].twinx()
    ax2.plot(x_col, buy_line, color='forestgreen', marker='o', linestyle='-', label="Median buy cost")
    ax2.plot(x_col, rent_line, color='darkred', marker='o', linestyle='-', label="Median rent cost")
    ax2.set_ylabel("Cost (USD)", color='black')
    ax2.legend(loc="best")
    plt.title("Vacancy & Cost", fontsize=14, fontweight="bold")
    
    ax[1].bar(x_col, y2_col, color='tan', label="Median home value")
    ax[1].set_xlabel("City", fontsize=14)
    ax[1].set_xticklabels(x_col, rotation=85)
    ax[1].set_ylabel("Home Value (USD)", color='black')
    ax[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f"{int(x/1000)}K"))    
    ax[1].legend(loc="upper left")
    
    ax4 = ax[1].twinx()
    ax4.plot(x_col, buy_line, color='forestgreen', marker='o', linestyle='-', label="Median buy cost")
    ax4.plot(x_col, rent_line, color='darkred', marker='o', linestyle='-', label="Median rent cost")
    ax4.set_ylabel("Cost (USD)", color='black')
    ax4.legend(loc="best")
    plt.title("Home Value & Cost", fontsize=14, fontweight="bold")
    plt.show()

if __name__ == "__main__":
    base_inputs = {"length_of_stay": 2.333, "monthly_rent": 1200, "home_price": 300000, "down_payment": 60000, "mortgage_rate": 5.0, "investment_interest_rate": 4.0}
    print(compare_rent_vs_buy(**base_inputs))
    plot_sensitivity_analysis(base_inputs)
    plot_vacancy("data/USA DP04 vacancy value cost.csv")

