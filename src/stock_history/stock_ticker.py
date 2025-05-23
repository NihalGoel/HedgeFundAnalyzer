import yfinance as yf

def get_average_price_per_quarter(ticker, quarter, year):
    quarter_dates = {
        1: ('01-01', '03-31'),
        2: ('04-01', '06-30'),
        3: ('07-01', '09-30'),
        4: ('10-01', '12-31')
    }

    if quarter not in quarter_dates:
        raise ValueError("Quarter must be an integer between 1 and 4.")

    start_suffix, end_suffix = quarter_dates[quarter]
    start_date = f"{year}-{start_suffix}"
    end_date = f"{year}-{end_suffix}"

    data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    if data.empty:
        return None

    return data["Close"].mean().item()

if __name__ == "__main__":
    average_price = get_average_price_per_quarter("AAPL", 2, 2023)
    print(f"Average price for Q2 2023: {average_price}")