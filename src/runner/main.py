from dataroma.latest_quarter_buys import get_latest_quarter_buys
from dataroma.scraper import get_fund_urls
from dataroma.historical_holdings import get_historical_holdings_matrix
from performance_calc.fund_performance import *
from runner.config import startYear, firstFundIndex, lastFundIndex
from stock_history.spy_data import get_spy_cum_returns
import pandas as pd

pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.width", 0)  # Auto-wrap wide output

# Calculates tables for hedge fund cumulative performance and compares it to SPY performance
def calculate_fund_performance():
    funds = get_fund_urls()
    all_funds_annual = []
    spy_df = get_spy_cum_returns(startYear)

    for fund in funds[
                firstFundIndex:lastFundIndex]:  # Scrapes fund indices x through y (Python slices are exclusive on the right)
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

def find_buy_opportunities():
    funds = get_fund_urls()
    buy_activities = []

    for fund in funds[firstFundIndex:lastFundIndex]:  # Scrapes fund indices x through y (Python slices are exclusive on the right)
        buy_activities.append(get_latest_quarter_buys(fund['url']))

    print("\n" + "=" * 80)
    print(f"{'Ticker':<10} {'Company':<35} {'% Portfolio':<12} {'Activity':<20}")
    print("-" * 80)

    for fund_buys in buy_activities:
        for stock in fund_buys:
            ticker = stock['ticker'].split()[0]  # Extract ticker only
            print(f"{ticker:<10} {stock['company']:<35} {stock['percentage']:<12} {stock['activity']:<20}")


if __name__ == "__main__":
    # calculate_fund_performance()
    find_buy_opportunities()