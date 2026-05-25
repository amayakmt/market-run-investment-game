import yfinance as yf
from config import STOCKS, ETFS, DATA_END
from pathlib import Path
from tqdm import tqdm

stocks_dir = Path("cache/stocks")
etfs_dir = Path("cache/etfs")

def download_assets():
    make_dirs()
    download_stocks()
    download_etfs()

def download_stocks():
    for stock in STOCKS:
        stock_path = stocks_dir / f"{stock}.parquet"
        if stock_path.exists():
            continue
        df = yf.download(
            tickers = stock,
            start = STOCKS[stock]["available_from"],
            end = DATA_END,
            interval = "1d",
            auto_adjust = True
        )
        df.columns = ['_'.join(col).strip() for col in df.columns.values]
        df.to_parquet(stock_path)

def download_etfs():
    for etf in ETFS:
        etf_path = etfs_dir / f"{etf}.parquet"
        if etf_path.exists():
            continue
        df = yf.download(
            tickers = etf,
            start = ETFS[etf]["available_from"],
            end = DATA_END,
            interval = "1d",
            auto_adjust = True
        )
        df.columns = ['_'.join(col).strip() for col in df.columns.values]
        df.to_parquet(etf_path)

def make_dirs():
    stocks_dir.mkdir(parents=True, exist_ok=True)
    etfs_dir.mkdir(parents=True, exist_ok=True)