import yfinance as yf
import pandas as pd
from joblib import Memory
pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.max_rows", None)  # Show a
pd.set_option("display.width", 0)  # Auto-wrap wide output

memory = Memory(".cache", verbose=0)

@memory.cache
def get_etf_returns(etf_tickers, period="5y"):
    returns = []

    for ticker in etf_tickers:
        try:
            data = yf.download(ticker, period=period, progress=False)
            if data.empty:
                continue

            start_price = data["Close"].iloc[0].item()
            end_price = data["Close"].iloc[-1].item()
            return_pct = ((end_price - start_price) / start_price) * 100

            returns.append({
                "Ticker": ticker,
                "Return (%)": round(return_pct, 2)
            })
        except Exception as e:
            print(f"Error with {ticker}: {e}")

    df = pd.DataFrame(returns)
    return df.sort_values(by="Return (%)", ascending=False)


# Example: A few iShares tickers (replace or expand this list)
def main():
    ishares_etfs = [
        "IVV",
        "IEFA",
        "IEMG",
        "AGG",
        "IWF",
        "IWD",
        "ITOT",
        "TLT",
        "SHY",
        "TIP",
        "LQD",
        "HYG",
        "EMB",
        "IWB",
        "IWM",
        "IWR",
        "IWN",
        "IWO",
        "IWS",
        "IWP",
        "IWV",
        "IJJ",
        "IJK",
        "IJS",
        "IJT",
        "IJR",
        "IJH",
        "IVW",
        "IVE",
        "IVZ",
        "IYZ",
        "IYF",
        "IYH",
        "IYJ",
        "IYK",
        "IYM",
        "IYT",
        "IYW",
        "IDU",
        "IUSG",
        "IUSV",
        "IUS",
        "IDV",
        "DVY",
        "SDY",
        "HDV",
        "VYM",
        "SPHD",
        "VIG",
        "SPY",
        "VOO",
        "VTI",
        "VEA",
        "VWO",
        "VXUS",
        "ACWI",
        "VT",
        "SPDW",
        "SPEM",
        "SPAB",
        "SPBO",
        "SPTI",
        "SPTL",
        "SPTS",
        "SPMB",
        "SPHY",
        "SPIP"
    ]

    top_etfs = get_etf_returns(ishares_etfs)
    print(top_etfs)


if __name__ == "__main__":
    main()