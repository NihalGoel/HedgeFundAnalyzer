import yfinance as yf
from joblib import Memory

memory = Memory(".cache", verbose=0)

@memory.cache
def get_spy_cum_returns(start_year, end_year=2025):
    spy = yf.download("SPY", start=f"{start_year - 1}-01-01", end=f"{end_year}-12-31", progress=False)
    annual_close = spy["Close"].resample("YE").last()
    spy_return = annual_close.pct_change().dropna() * 100
    spy_annual = spy_return.reset_index()
    spy_annual.columns = ["Date", "spy_return_pct"]
    spy_annual["year"] = spy_annual["Date"].dt.year
    spy_annual["cumulative_spy_return_pct"] = spy_annual["spy_return_pct"].cumsum()
    return spy_annual[["year", "spy_return_pct", "cumulative_spy_return_pct"]]