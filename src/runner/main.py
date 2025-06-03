from dataroma.latest_quarter_buys import get_latest_quarter_buys
from dataroma.scraper import get_fund_urls
from dataroma.historical_holdings import get_historical_holdings_matrix
from performance_calc.fund_performance import *
from runner.config import startYear, firstFundIndex, lastFundIndex
from stock_history.spy_data import get_spy_cum_returns
from stock_history.stock_ticker import is_price_declining, get_decline_from_104wk_high
import pandas as pd
import time

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

def filter_buys_with_decline_info(buy_activities):
    filtered_buys = []
    for fund_buys in buy_activities:
        for stock in fund_buys:
            decline = is_price_declining(stock['ticker'].split()[0], quarter=2)
            decline_104wk = get_decline_from_104wk_high(stock['ticker'].split()[0])
            if decline is not None:
                stock['decline_pct'] = decline
                stock['decline_104wk'] = decline_104wk
                filtered_buys.append(stock)
    return filtered_buys

def find_buy_opportunities():
    funds = get_fund_urls()
    buy_activities = []

    for fund in funds[firstFundIndex:lastFundIndex]:  # Scrapes fund indices x through y (Python slices are exclusive on the right)
        buy_activities.append(get_latest_quarter_buys(fund))

    filtered_buys = filter_buys_with_decline_info(buy_activities)

    filtered_buys.sort(key=lambda x: float(x['value']), reverse=True)

    print("\n" + "=" * 150)
    print(f"{'Ticker':<10} {'Company':<30} {'% Port':<10} {'Activity':<15} {'% Decl':<9} {'% 2yr':<9} {'Position':<15} {'Fund':<30}")
    print("-" * 150)

    for stock in filtered_buys:
        ticker = stock['ticker'].split()[0]
        print(f"{ticker:<10} "
              f"{stock['company']:<30}"
              f" {stock['percentage']:<10}"
              f" {stock['activity']:<15}"
              f" {stock['decline_pct']:<9.2f}"
              f" {stock['decline_104wk']:<9.2f}"
              f" {stock['value_mil']:<15}"
              f" {stock['fund']:<30}")


if __name__ == "__main__":
    start = time.perf_counter()
    # calculate_fund_performance()
    find_buy_opportunities()
    end = time.perf_counter()
    print(f"Execution time: {end - start:.4f} seconds")

