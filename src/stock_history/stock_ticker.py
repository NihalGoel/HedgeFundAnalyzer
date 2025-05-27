import yfinance as yf
from functools import lru_cache
from typing import Optional
from datetime import datetime, timedelta

def is_price_declining(ticker, quarter, year=2025) -> Optional[float]:
    if quarter == 1:
        prev_quarter = 4
        prev_year = year - 1
    else:
        prev_quarter = quarter - 1
        prev_year = year

    current_avg = get_average_price_per_quarter(ticker, quarter, year)
    prev_avg = get_average_price_per_quarter(ticker, prev_quarter, prev_year)

    if current_avg is None or prev_avg is None:
        return None

    if current_avg < prev_avg:
        decline_pct = ((prev_avg - current_avg) / prev_avg) * 100
        return round(decline_pct, 2)
    return None

@lru_cache(maxsize=None)
def get_average_price_per_quarter(ticker, quarter, year=2025) -> float:
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

def get_decline_from_104wk_high(ticker: str) -> Optional[float]:
    today = datetime.today()
    start_date = today - timedelta(weeks=104)
    data = yf.download(ticker, start=start_date.strftime('%Y-%m-%d'), end=today.strftime('%Y-%m-%d'), progress=False)

    if data.empty:
        return None

    high_104wk = data["High"].max().item()
    current_price = data["Close"].iloc[-1].item()

    if high_104wk == 0:
        return None

    decline_pct = ((high_104wk - current_price) / high_104wk) * 100
    return round(decline_pct, 2)