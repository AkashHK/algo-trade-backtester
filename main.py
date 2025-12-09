import yfinance as yf
import pandas as pd
import numpy as np

def fetch_data(ticker, start_date, end_date):
    """
    Fetches OHLCV data from Yahoo Finance.
    auto_adjust=True ensures we account for splits/dividends.
    """
    print(f"Fetching {ticker} data...")
    try:
        df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True, progress=False)
        return df.dropna()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

def backtest(df, short_window=50, long_window=200):
    """
    Runs a vectorized Golden Cross strategy.
    
    Logic:
    - Buy (1) when SMA_50 > SMA_200
    - Sell/Flat (0) otherwise
    """
    # Calculate indicators
    df['SMA_50'] = df['Close'].rolling(window=short_window).mean()
    df['SMA_200'] = df['Close'].rolling(window=long_window).mean()
    
    # Vectorized signal generation using numpy (much faster than iterating rows)
    df['Signal'] = np.where(df['SMA_50'] > df['SMA_200'], 1.0, 0.0)
    
    # Calculate returns
    df['Market_Return'] = df['Close'].pct_change()
    
    # IMPORTANT: Shift signal by 1. We make the decision at Close t, 
    # but execute at Open t+1. Without shift, this introduces look-ahead bias.
    df['Strategy_Return'] = df['Market_Return'] * df['Signal'].shift(1)
    
    return df.dropna().copy()

def calculate_metrics(df):
    """Returns Sharpe Ratio, Cumulative Return, and Max Drawdown."""
    
    # 1. Sharpe Ratio (Annualized, assuming 252 trading days)
    daily_mean = df['Strategy_Return'].mean()
    daily_std = df['Strategy_Return'].std()
    
    if daily_std == 0:
        return 0.0, 0.0, 0.0
        
    sharpe = (daily_mean / daily_std) * np.sqrt(252)
    
    # 2. Cumulative Return
    df['Cumulative_Return'] = (1 + df['Strategy_Return']).cumprod()
    total_return = df['Cumulative_Return'].iloc[-1] - 1
    
    # 3. Max Drawdown
    # Compute running peak to find the deepest valley
    running_max = df['Cumulative_Return'].cummax()
    drawdown = df['Cumulative_Return'] / running_max - 1
    max_dd = drawdown.min()
    
    return sharpe, total_return, max_dd

if __name__ == "__main__":
    # Config
    SYMBOL = "SPY"
    START = "2020-01-01"
    END = "2025-01-01"
    
    # Execution Pipeline
    data = fetch_data(SYMBOL, START, END)
    
    if not data.empty:
        results = backtest(data)
        sharpe, total_ret, max_dd = calculate_metrics(results)
        
        print(f"\n--- Backtest Results: {SYMBOL} ---")
        print(f"Total Return: {total_ret:.2%}")
        print(f"Sharpe Ratio: {sharpe:.2f}")
        print(f"Max Drawdown: {max_dd:.2%}")
        
        # Save for manual verification
        results.to_csv("backtest_debug.csv")
    else:
        print("No data found.")
