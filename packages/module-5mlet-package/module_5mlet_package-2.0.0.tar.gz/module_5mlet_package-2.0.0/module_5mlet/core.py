# main.py

import investments

initial_value = 1000
final_value = 1500
years = 5
annual_rate = 6

investment_return = investments.calculate_investment_return(initial_value, final_value)
print(f"Investment return: {investment_return:.2f}%")

final_value_with_interest = investments.calculate_compound_interest(initial_value, annual_rate, years)
print(f"Final value with compound interest: ${final_value_with_interest:.2f}")

monthly_rate = investments.convert_annual_rate_to_monthly(annual_rate)
print(f"Monthly interest rate: {monthly_rate:.2f}%")

cagr = investments.calculate_cagr(initial_value, final_value, years)
print(f"CAGR: {cagr:.2f}%")
