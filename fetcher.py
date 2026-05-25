import yfinance as yf
from config import STOCKS, ETFS, DATA_END
from pathlib import Path
from tqdm import tqdm

stocks_dir = Path("cache/stocks")
etfs_dir = Path("cache/etfs")

def download_assets():
    print("DOWNLOADING REQUIRED ASSETS...")
    make_dirs()
    download_stocks()
    download_etfs()
    print("SUCCESS")

def make_dirs():
    stocks_dir.mkdir(parents=True, exist_ok=True)
    etfs_dir.mkdir(parents=True, exist_ok=True)

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
