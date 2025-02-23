import numpy as np
import matplotlib.pyplot as plt
import Calculator

# Updated to align with modifications in the compare_rent_vs_buy function, ensuring consistency in analysis.
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
            result = Calculator.compare_rent_vs_buy(**inputs)
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

plot_sensitivity_analysis(Calculator.inputs)