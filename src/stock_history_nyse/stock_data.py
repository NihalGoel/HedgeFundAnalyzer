import yfinance as yf

def get_historical_stock_data(ticker, period="1y", interval="1wk"):
    """
    Fetch historical stock data for a given ticker.
    period: e.g., '1y', '6mo', '5d'
    interval: e.g., '1d', '1wk', '1mo'
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)
        return hist.reset_index().to_dict(orient="records")
    except Exception as e:
        print(f"Failed to get data for {ticker}: {e}")
        return []

if __name__ == "__main__":
    data = get_historical_stock_data("AAPL", period="1y", interval="1mo")
    for entry in data[:5]:  # print first 5 rows to check
        print(entry)
