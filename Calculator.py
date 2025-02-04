def compare_rent_vs_buy(length_of_stay, monthly_rent, home_price, down_payment, mortgage_rate, property_tax_rate=1.2, maintenance_rate=1.0):
    """
    Compare renting vs. buying a home.
    
    :param length_of_stay: Years planning to stay in the home
    :param monthly_rent: Monthly rent cost
    :param home_price: Purchase price of the home
    :param down_payment: Initial down payment amount
    :param mortgage_rate: Annual mortgage interest rate (as percentage)
    :param property_tax_rate: Annual property tax rate (default 1.2%)
    :param maintenance_rate: Annual maintenance cost rate (default 1.0%)
    :return: Total costs for renting and buying, and recommendation
    """
    import numpy as np
    
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

# Example Usage
inputs = {
    "length_of_stay": 10,  # years
    "monthly_rent": 2000,  # dollars
    "home_price": 500000,  # dollars
    "down_payment": 100000,  # dollars
    "mortgage_rate": 5.0  # percent
}

result = compare_rent_vs_buy(**inputs)
print(result)
