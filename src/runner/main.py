from dataroma.scraper import get_fund_urls
from dataroma.scraper import get_historical_holdings_matrix
from performance_calc.fund_performance import *
from runner.config import startYear, firstFundIndex, lastFundIndex, maxHoldingCount
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

        if len(set(h['ticker'] for h in holdings)) > maxHoldingCount:
            print(f"Skipping {fund['name']} — too many holdings ({len(holdings)})")
            continue

        annual_df = calculate_annual_pnl(holdings)
        merged_df = pd.merge(annual_df, spy_df, on="year", how="left")

        all_funds_annual.append(fund['name'])
        all_funds_annual.append(merged_df)

    for fund_performance in all_funds_annual:
        print("\n" + "=" * 80)
        print(fund_performance)