import yfinance as yf
import pandas as pd

def fetch_data(ticker, start_date, end_date):
    print(f"Downloading data for {ticker}...")
    # download() fetches Open, High, Low, Close, Volume
    df = yf.download(ticker, start=start_date, end=end_date)
    
    # Clean up: Drop any rows where data is missing (common in finance)
    df = df.dropna()
    
    return df

if __name__ == "__main__":
    # Test with S&P 500 (SPY) for the last 5 years
    symbol = "SPY"
    data = fetch_data(symbol, "2020-01-01", "2025-01-01")
    
    print("\n--- DATA PREVIEW ---")
    print(data.head())
    print(f"\nTotal Rows: {len(data)}")
