import numpy as np
import matplotlib.pyplot as plt

def compare_rent_vs_buy(length_of_stay, monthly_rent, home_price, down_payment, mortgage_rate, property_tax_rate=1.2, maintenance_rate=1.0):
    """
    Compare renting vs. buying a home.
    """
    # Renting total cost
    total_rent_cost = monthly_rent * 12 * length_of_stay
    
    # Buying costs
    loan_amount = home_price - down_payment
    monthly_interest_rate = (mortgage_rate / 100) / 12
    num_payments = length_of_stay * 12
    
    if monthly_interest_rate > 0:
        monthly_mortgage_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** num_payments) / ((1 + monthly_interest_rate) ** num_payments - 1)
    else:
        monthly_mortgage_payment = loan_amount / num_payments
    
    total_mortgage_cost = monthly_mortgage_payment * num_payments
    total_property_tax = (property_tax_rate / 100) * home_price * length_of_stay
    total_maintenance = (maintenance_rate / 100) * home_price * length_of_stay
    
    total_buy_cost = down_payment + total_mortgage_cost + total_property_tax + total_maintenance
    
    # Recommendation
    if total_rent_cost < total_buy_cost:
        recommendation = "Renting is financially better."
    else:
        recommendation = "Buying is financially better."
    
    return {
        "Total Rent Cost": total_rent_cost,
        "Total Buy Cost": total_buy_cost,
        "Recommendation": recommendation
    }

def plot_sensitivity_analysis(base_inputs):
    """
    Plots how the total rent and buy costs change when varying one input factor at a time.
    """
    factors = {
        "length_of_stay": (1, base_inputs["length_of_stay"], 1),
        "monthly_rent": (0, base_inputs["monthly_rent"], 100),
        "home_price": (0, base_inputs["home_price"], 1000),
        "down_payment": (0, base_inputs["down_payment"], 1000),
        "mortgage_rate": (0, base_inputs["mortgage_rate"], 0.5)
    }
    
    for factor, (start, stop, step) in factors.items():
        values = np.arange(start, stop + step, step)
        rent_costs, buy_costs = [], []
        
        for value in values:
            inputs = base_inputs.copy()
            inputs[factor] = value
            result = compare_rent_vs_buy(**inputs)
            rent_costs.append(result["Total Rent Cost"])
            buy_costs.append(result["Total Buy Cost"])
        
        plt.figure(figsize=(8, 5))
        plt.plot(values, rent_costs, label='Total Rent Cost', marker='o')
        plt.plot(values, buy_costs, label='Total Buy Cost', marker='s')
        plt.xlabel(factor.replace("_", " ").title())
        plt.ylabel("Cost (USD)")
        plt.title(f"Impact of {factor.replace('_', ' ').title()} on Rent vs. Buy Cost")
        plt.legend()
        plt.grid()
        plt.show()

# Example Usage
inputs = {
    "length_of_stay": 10,
    "monthly_rent": 2000,
    "home_price": 500000,
    "down_payment": 100000,
    "mortgage_rate": 5.0
}
result = compare_rent_vs_buy(**inputs)
print(result)

# Plot Sensitivity Analysis
plot_sensitivity_analysis(inputs)
