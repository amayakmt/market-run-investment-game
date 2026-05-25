STARTING_CASH    = 10_000.00
FEE_MIN          = 0.35
FEE_RATE         = 0.0005   
GTC_EXPIRY_WEEKS = 3
MAX_OPEN_ORDERS  = 10
MAX_WATCHLIST    = 10
DATA_END = "2020-12-31"

GAME_LENGTHS = {
    "Sprint":   30,
    "Standard": 52,
    "Marathon": 104,
}

BLACK_SWAN_PROB = {
    "Easy":   0.000,
    "Normal": 0.003,
    "Hard":   0.008,
    "Expert": 0.015,
}

STOCKS = {
    "AAPL": {"name": "Apple Inc.", "sector": "Technology", "available_from": "1980-12-12"},
    "MSFT": {"name": "Microsoft Corp.", "sector": "Technology", "available_from": "1986-03-13"},
    "GOOGL": {"name": "Alphabet Inc.", "sector": "Technology", "available_from": "2004-08-19"},
    "AMZN": {"name": "Amazon.com Inc.", "sector": "Technology", "available_from": "1997-05-15"},
    "NVDA": {"name": "NVIDIA Corp.", "sector": "Technology", "available_from": "1999-01-22"},
    "META": {"name": "Meta Platforms", "sector": "Technology", "available_from": "2012-05-18"},
    "JPM": {"name": "JPMorgan Chase", "sector": "Financials", "available_from": "1980-03-17"},
    "BAC": {"name": "Bank of America", "sector": "Financials", "available_from": "1973-02-21"},
    "V": {"name": "Visa Inc.", "sector": "Financials", "available_from": "2008-03-19"},
    "MA": {"name": "Mastercard", "sector": "Financials", "available_from": "2006-05-25"},
    "JNJ": {"name": "Johnson & Johnson", "sector": "Healthcare", "available_from": "1962-01-02"},
    "UNH": {"name": "UnitedHealth Group", "sector": "Healthcare", "available_from": "1984-10-17"},
    "LLY": {"name": "Eli Lilly", "sector": "Healthcare", "available_from": "1972-06-01"},
    "ABBV": {"name": "AbbVie Inc.", "sector": "Healthcare", "available_from": "2013-01-02"},
    "TSLA": {"name": "Tesla Inc.", "sector": "Consumer Discretionary", "available_from": "2010-06-29"},
    "HD": {"name": "Home Depot", "sector": "Consumer Discretionary", "available_from": "1981-09-22"},
    "MCD": {"name": "McDonald's Corp.", "sector": "Consumer Discretionary", "available_from": "1966-07-05"},
    "PG": {"name": "Procter & Gamble", "sector": "Consumer Discretionary", "available_from": "1962-01-02"},
    "COST": {"name": "Costco Wholesale", "sector": "Consumer Discretionary", "available_from": "1986-07-09"},
    "XOM": {"name": "Exxon Mobil", "sector": "Energy", "available_from": "1962-01-02"},
    "CVX": {"name": "Chevron Corp.", "sector": "Energy", "available_from": "1962-01-02"},
    "CAT": {"name": "Caterpillar Inc.", "sector": "Industrials", "available_from": "1962-01-02"},
    "BA": {"name": "Boeing Co.", "sector": "Industrials", "available_from": "1962-01-02"},
    "VZ": {"name": "Verizon Communications", "sector": "Telecom / Other", "available_from": "1983-11-21"},
    "BRK-B": {"name": "Berkshire Hathaway B", "sector": "Other", "available_from": "1996-05-09"},
}

ETFS = {
    "SPY": {"name": "S&P 500 Index", "available_from": "1993-01-29"},
    "QQQ": {"name": "NASDAQ 100", "available_from": "1999-03-10"},
    "IWM": {"name": "Russell 2000", "available_from": "2000-05-26"},
    "GLD": {"name": "Gold", "available_from": "2004-11-18"},
    "TLT": {"name": "20+ Year Treasury Bonds", "available_from": "2002-07-30"},
}