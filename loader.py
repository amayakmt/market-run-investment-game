import pandas as pd
from pathlib import Path

stocks_dir = Path("cache/stocks")
etfs_dir = Path("cache/etfs")

def load_asset(ticker):
    ticker_parquet_path = f"{ticker}.parquet"
    stock_path = stocks_dir / ticker_parquet_path
    etf_path = etfs_dir / ticker_parquet_path
    if stock_path.exists():
        df = pd.read_parquet(stock_path)
    elif etf_path.exists():
        df = pd.read_parquet(etf_path)
    else:
        raise FileNotFoundError(f"ticker {ticker} not found in the assets")
    df = df.rename(columns={
        f'Close_{ticker}': 'Close',
        f'High_{ticker}': 'High',
        f'Low_{ticker}': 'Low',
        f'Open_{ticker}': 'Open',
        f'Volume_{ticker}': 'Volume'
    })
    return df

def resample_weekly(ticker):
    df = load_asset(ticker)
    df = df.resample('W-FRI').agg(
        Close=('Close', 'last'),
        High=('High', 'max'),
        Low=('Low', 'min'),
        Open=('Open', 'first'),
        Volume=('Volume', 'sum')
        )
    return df
    