from dataroma.latest_quarter_buys import get_latest_quarter_buys
from dataroma.scraper import get_fund_urls
from dataroma.historical_holdings import get_historical_holdings_matrix
from performance_calc.fund_performance import *
from runner.config import startYear, firstFundIndex, lastFundIndex
from stock_history.spy_data import get_spy_cum_returns
from stock_history.stock_ticker import is_price_declining, get_decline_from_104wk_high
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
        buy_activities.append(get_latest_quarter_buys(fund))

    filtered_buys = []
    for fund_buys in buy_activities:
        for stock in fund_buys:
            decline = is_price_declining(stock['ticker'].split()[0], quarter=2)
            decline_104wk = get_decline_from_104wk_high(stock['ticker'].split()[0])
            if decline is not None:
                stock['decline_pct'] = decline
                stock['decline_104wk'] = decline_104wk
                filtered_buys.append(stock)

    filtered_buys.sort(key=lambda x: float(x['decline_104wk']), reverse=True)

    print("\n" + "=" * 180)
    print(f"{'Ticker':<10} {'Company':<45} {'% Portfolio':<14} {'Activity':<20} {'% Decline':<12} {'% 2yr Decline':<15} {'Fund':<40}")
    print("-" * 180)

    for stock in filtered_buys:
        ticker = stock['ticker'].split()[0]
        print(f"{ticker:<10} {stock['company']:<45} {stock['percentage']:<14} {stock['activity']:<20} {stock['decline_pct']:<12.2f} {stock['decline_104wk']:<15.2f} {stock['fund']:<40}")


if __name__ == "__main__":
    # calculate_fund_performance()
    find_buy_opportunities()