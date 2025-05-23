import yfinance as yf

def get_spy_cum_returns(start_year, end_year=2025):
    spy = yf.download("SPY", start=f"{start_year}-01-01", end=f"{end_year}-12-31", progress=False)
    spy["Year"] = spy.index.year
    spy_annual = spy["Close"].resample("Y").last().pct_change().dropna().reset_index()
    spy_annual["year"] = spy_annual["Date"].dt.year
    spy_annual["spy_return_pct"] = spy_annual["Close"] * 100
    spy_annual["cumulative_spy_return_pct"] = spy_annual["spy_return_pct"].cumsum()
    final_return = spy_annual["cumulative_spy_return_pct"].iloc[-1]
    return final_return
# todo fix method