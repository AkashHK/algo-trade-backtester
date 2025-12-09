# Vectorized Backtester

A simple, vectorized backtesting engine for S&P 500 strategies using Pandas and NumPy. This implementation uses `numpy.where` and vector operations to process signals instantly across the entire dataframe.

## Strategy Logic
**Golden Cross:**
* Buy when 50-day SMA > 200-day SMA.
* Sell/Flat otherwise.
* **Note:** Signals are shifted by 1 day to prevent look-ahead bias (simulating execution on the next day's open).

## Setup & Usage

1. **Install dependencies:**
   ```bash
   pip install pandas numpy yfinance