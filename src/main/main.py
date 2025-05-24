from dataroma.scraper import get_fund_urls
from dataroma.scraper import get_historical_holdings_matrix
from performance_calc.fund_performance import *
from stock_history.spy_data import get_spy_cum_returns
import pandas as pd

pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.width", 0)  # Auto-wrap wide output

if __name__ == "__main__":
    funds = get_fund_urls()
    all_funds_annual = []
    for fund in funds[1:50]:  # Scrapes fund indices 4 through 9 (Python slices are exclusive on the right)
        print(f"Scraping holdings for {fund['name']}...")
        holdings = get_historical_holdings_matrix(fund['url'])
        if len(set(h['ticker'] for h in holdings)) > 350:
            print(f"Skipping {fund['name']} — too many holdings ({len(holdings)})")
            continue
        pnl_results = calculate_quarterly_pnl(holdings)
        annual_df = calculate_annual_pnl(pnl_results)
        annual_df["cumulative_return_pct"] = annual_df["annual_return_pct"].cumsum()
        spy_df = get_spy_cum_returns(startYear)
        merged_df = pd.merge(annual_df, spy_df, on="year", how="left")
        fund_name = fund['name']
        all_funds_annual.append(fund_name)
        all_funds_annual.append(merged_df)

    for fund_perf in all_funds_annual:
        print("\n" + "=" * 80)
        print(fund_perf)