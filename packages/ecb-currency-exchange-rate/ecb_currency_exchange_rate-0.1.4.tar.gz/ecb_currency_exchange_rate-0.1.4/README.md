# ECB Exchange Rates

A Python package to fetches the exchange rate for a given date, from currency, and to currency.

This package uses daily exchange rate published by ECB.
[ECB page for Euro foreign exchange reference rates](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html)

The ECB exchange rate data does **not** include weekends.
If the date falls on a weekend or holiday, it uses the last available rate.

## Installation

```sh
pip install ecb-currency-exchange-rate
```

## Usage

### Single time conversion
```Python
from ecb_rates import ecb_rates

rate = ecb_rates.get_exchange_rate("2025-03-31", "EUR", "USD")
print(rate)
```
### Batch conversion: different dates for fixed currency exchange pair with pandas DataFrame.

```Python

from ecb_rates import ecb_rates
# Assuming df has 'transaction_date' and 'usd_amount' columns
df = pd.DataFrame({
    'transaction_date': ['2025-04-01', '2025-04-02', '2025-04-03'],
    'usd_amount': [100, 150, 200]
})

# Convert from USD to EUR starting from '2025-04-01' with custom column names
converted_df = convert_currency_amounts(df, 'USD', 'EUR', start_date='2025-04-01', 
                                         date_column='transaction_date', amount_column='usd_amount')
print(converted_df)

```