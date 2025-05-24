from dataroma.scraper import get_fund_urls
from dataroma.scraper import get_historical_holdings_matrix
from performance_calc.fund_performance import *
from runner.config import startYear, firstFundIndex, lastFundIndex
from stock_history.spy_data import get_spy_cum_returns
import pandas as pd

pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.width", 0)  # Auto-wrap wide output

if __name__ == "__main__":
    funds = get_fund_urls()
    all_funds_annual = []
    spy_df = get_spy_cum_returns(startYear)

    for fund in funds[firstFundIndex:lastFundIndex]:  # Scrapes fund indices x through y (Python slices are exclusive on the right)
        print(f"Scraping holdings for {fund['name']}...")
        holdings = get_historical_holdings_matrix(fund['url'])

        annual_df = calculate_annual_pnl(holdings)
        merged_df = pd.merge(annual_df, spy_df, on="year", how="left")

        all_funds_annual.append((fund['name'], merged_df))

    all_funds_annual.sort(
        key=lambda x: x[1]["annual_return_cumulative"].iloc[-1] if not x[1].empty else float('-inf'),
        reverse=True
    )

    for fund_name, fund_performance in all_funds_annual:
        print("\n" + "=" * 80)
        print(f"{fund_name}")
        print(fund_performance)