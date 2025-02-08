def compare_rent_vs_buy(length_of_stay, monthly_rent, home_price, down_payment, mortgage_rate, investment_interest_rate, property_tax_rate=1.2, maintenance_rate=1.0, selling_cost_rate=8.0): # Added new parameters...JMR
    """
    Compare renting vs. buying a home.
    
    :param length_of_stay: Years planning to stay in the home
    :param monthly_rent: Monthly rent cost
    :param home_price: Purchase price of the home
    :param down_payment: Initial down payment amount
    :param mortgage_rate: Annual mortgage interest rate (as percentage)
    :param property_tax_rate: Annual property tax rate (default 1.2%)
    :param maintenance_rate: Annual maintenance cost rate (default 1.0%)
    :param investment_interest_rate: Annual investment interest (as percentage)  ...Added parameter...JMR
    :param selling_cost_rate: Cumulative costs of selling a home (default 8.0%)...Added parameter...JMR
    :return: Total costs for renting and buying, and recommendation
    """
    import numpy as np
    
    # Renting total cost
    investment = (down_payment * (investment_interest_rate / 100)) * length_of_stay # Added a financial return estimate for investing the down payment amount...JMR
    total_rent_cost = (monthly_rent * 12 * length_of_stay) - investment # Added investment calculation to total_rent_cost...JMR
    
    # Buying costs
    loan_amount = home_price - down_payment
    monthly_interest_rate = (mortgage_rate / 100) / 12
    num_payments = length_of_stay * 12
    home_appreciation = home_price * (1 + (investment_interest_rate / 100) / 12)**(12 * length_of_stay) # Added home appreciation value...JMR
    selling_costs = home_appreciation * (selling_cost_rate / 100)    
    
    if monthly_interest_rate > 0:
        monthly_mortgage_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** num_payments) / ((1 + monthly_interest_rate) ** num_payments - 1)
    else:
        monthly_mortgage_payment = loan_amount / num_payments
    
    total_mortgage_cost = monthly_mortgage_payment * num_payments
    total_property_tax = (property_tax_rate / 100) * home_price * length_of_stay
    total_maintenance = (maintenance_rate / 100) * home_price * length_of_stay
    total_resale_value = home_appreciation - selling_costs # Added a financial return estimate for sale of home...JMR
    
    total_buy_cost = down_payment + total_mortgage_cost + total_property_tax + total_maintenance - total_resale_value # Subtracted resale value of home from buying costs...JMR
    
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

# Example Usage
inputs = {
    "length_of_stay": 10,  # years
    "monthly_rent": 2000,  # dollars
    "home_price": 500000,  # dollars
    "down_payment": 100000,  # dollars
    "mortgage_rate": 5.0,  # percent
    "investment_interest_rate": 4.0 # percent ...Added new input...JMR
    }

result = compare_rent_vs_buy(**inputs)
print(result)

