# 💰 My Investment

My Investment is a simple and easy-to-use Python library for performing common financial calculations related to investments, such as return on investment, compound interest, monthly interest rate conversion, and CAGR (Compound Annual Growth Rate).

## 📦 Installation

Install the package using `pip`:

```sh
pip install module-5mlet-package
```
> 💡 Note: Make sure you have Python 3.7+ installed.

## 🚀 Usage

Here's a basic example of how to use the library:

```py
from investments import calculate_investment_return, calculate_compound_interest

initial_value = 1000
final_value = 1500

# Calculate investment return
investment_return = calculate_investment_return(initial_value, final_value)
print(f"Investment return: {investment_return:.2f}%")

# Calculate compound interest
final_with_interest = calculate_compound_interest(initial_value, 6, 5)
print(f"Final value with compound interest: ${final_with_interest:.2f}")
```

## 📚 Features

* `calculate_investment_return()`: Calculates the total return of an investment.

* `calculate_compound_interest()`: Computes final amount using compound interest.

* `convert_annual_rate_to_monthly()`: Converts an annual interest rate to a monthly one.

* `calculate_cagr()`: Calculates the Compound Annual Growth Rate.

## 🧪 Running Tests

You can run the unit tests using:

```bash
python -m unittest discover tests
```

## 📄 License

This project is licensed under the MIT License.