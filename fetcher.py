import yfinance as yf
from config import STOCKS, ETFS, DATA_END
from pathlib import Path
from tqdm import tqdm
import pandas as pd

stocks_dir = Path("cache/stocks")
etfs_dir = Path("cache/etfs")

# DOWNLOAD ------------------------------------------- |

def download_assets():
    print("DOWNLOADING REQUIRED ASSETS...")
    make_dirs()
    download_stocks()
    download_etfs()
    print("SUCCESS")

def download_stocks():
    print("STOCK DATA:")
    for stock in tqdm(STOCKS):
        stock_path = stocks_dir / f"{stock}.parquet"
        if stock_path.exists():
            continue
        df = yf.download(
            tickers = stock,
            start = STOCKS[stock]["available_from"],
            end = DATA_END,
            interval = "1d",
            auto_adjust = True,
            progress = False
        )
        df.columns = ['_'.join(col).strip() for col in df.columns.values]
        df.to_parquet(stock_path)

def download_etfs():
    print("ETF DATA: ")
    for etf in tqdm(ETFS):
        etf_path = etfs_dir / f"{etf}.parquet"
        if etf_path.exists():
            continue
        df = yf.download(
            tickers = etf,
            start = ETFS[etf]["available_from"],
            end = DATA_END,
            interval = "1d",
            auto_adjust = True,
            progress = False
        )
        df.columns = ['_'.join(col).strip() for col in df.columns.values]
        df.to_parquet(etf_path)

def make_dirs():
    stocks_dir.mkdir(parents=True, exist_ok=True)
    etfs_dir.mkdir(parents=True, exist_ok=True)

# LOAD --------------------------------------------------- |

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
    