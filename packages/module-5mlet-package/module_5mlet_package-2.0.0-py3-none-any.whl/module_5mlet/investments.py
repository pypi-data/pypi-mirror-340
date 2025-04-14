# investments.py

def calculate_investment_return(initial_value, final_value):
    """
    Calculates the return on investment.

    Args:
        initial_value (float): Initial investment amount.
        final_value (float): Final investment amount.

    Returns:
        float: Investment return as a percentage.
    """
    investment_return = (final_value - initial_value) / initial_value * 100
    return investment_return

def calculate_compound_interest(principal, annual_interest_rate, periods):
    """
    Calculates the final value of an investment with compound interest.

    Args:
        principal (float): Initial amount invested.
        annual_interest_rate (float): Annual interest rate as a percentage.
        periods (int): Number of periods (years).

    Returns:
        float: Final value after the period with compound interest.
    """
    interest_rate_decimal = annual_interest_rate / 100
    final_value = principal * (1 + interest_rate_decimal) ** periods
    return final_value

def convert_annual_rate_to_monthly(annual_rate):
    """
    Converts an annual interest rate to a monthly rate.

    Args:
        annual_rate (float): Annual interest rate as a percentage.

    Returns:
        float: Monthly interest rate as a percentage.
    """
    monthly_rate = (1 + annual_rate / 100) ** (1 / 12) - 1
    return monthly_rate * 100

def calculate_cagr(initial_value, final_value, years):
    """
    Calculates the Compound Annual Growth Rate (CAGR).

    Args:
        initial_value (float): Initial investment amount.
        final_value (float): Final investment amount.
        years (int): Number of years.

    Returns:
        float: CAGR as a percentage.
    """
    cagr = ((final_value / initial_value) ** (1 / years) - 1) * 100
    return cagr
