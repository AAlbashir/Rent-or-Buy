import numpy as np
import matplotlib.pyplot as plt

# Added new parameters...JMR
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
...Added parameter...JMR    
    :param investment_interest_rate: Annual investment interest (as percentage) 
...Added parameter...JMR
    :param selling_cost_rate: Cumulative costs of selling a home (default 8.0%)
    :return: Total costs for renting and buying, and recommendation
    """
       
    # Renting total cost
# Added a financial return estimate for investing the down_payment amount...JMR
    investment = (down_payment * (investment_interest_rate / 100)) * length_of_stay 
# Added investment calculation to total_rent_cost...JMR
    total_rent_cost = (monthly_rent * 12 * length_of_stay) - investment
# Added rounded value to account for currency values...JMR
    final_rent_cost = round(total_rent_cost, 2)

    
    # Buying costs
    loan_amount = home_price - down_payment
    monthly_interest_rate = (mortgage_rate / 100) / 12
    num_payments = length_of_stay * 12
# Added the estimated future value of the home...JMR
    home_appreciation = home_price * (1 + (investment_interest_rate / 100) / 12)**(12 * length_of_stay) 
# Added the estimated costs of selling the home...JMR   
    selling_costs = home_appreciation * (selling_cost_rate / 100) 

    
    if monthly_interest_rate > 0:
        monthly_mortgage_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** num_payments) / ((1 + monthly_interest_rate) ** num_payments - 1)
    else:
        monthly_mortgage_payment = loan_amount / num_payments
    
    total_mortgage_cost = monthly_mortgage_payment * num_payments
    total_property_tax = (property_tax_rate / 100) * home_price * length_of_stay
    total_maintenance = (maintenance_rate / 100) * home_price * length_of_stay
# Added a financial return estimate for sale of the home...JMR
    total_resale_value = home_appreciation - selling_costs 

# Subtracted resale value of home from buying costs...JMR
    total_buy_cost = down_payment + total_mortgage_cost + total_property_tax + total_maintenance - total_resale_value
# Added rounded value to account for currency values...JMR
    final_buy_cost = round(total_buy_cost, 2)
    
    # Recommendation
    if final_rent_cost < final_buy_cost:
        recommendation = "Renting is financially better."
    elif final_rent_cost > final_buy_cost:
        recommendation = "Buying is financially better."
# Added new condition for equivalent costs...JMR 
    else:
        recommendation = "Either."
    
    return {
        "Rent Cost": final_rent_cost,
        "Buy Cost": final_buy_cost,
        "Recommendation": recommendation
    }
    
# Example Usage
"""
inputs = {
    "length_of_stay": 2.333,  # years
    "monthly_rent": 2000,  # dollars
    "home_price": 500000,  # dollars
    "down_payment": 100000,  # dollars
    "mortgage_rate": 5.0,  # percent
# ...Added new input...JMR
    "investment_interest_rate": 4.0 # percent 
    }

result = compare_rent_vs_buy(**inputs)
print(result)
"""

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
