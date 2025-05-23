from dataroma.scraper import get_fund_urls
from dataroma.scraper import get_historical_holdings_matrix
from performance_calc.fund_performance import *
from stock_history.spy_data import get_spy_cum_returns

if __name__ == "__main__":
    funds = get_fund_urls()
    all_funds_annual = []
    for fund in funds[:1]:  # Scrape first 2 funds for demo
        print(f"Scraping holdings for {fund['name']}...")
        holdings = get_historical_holdings_matrix(fund['url'])
        # performance = append_number_of_shares_to_holding(holdings)
        pnl_results = calculate_quarterly_pnl(holdings)
        annual_df = calculate_annual_pnl(pnl_results)
        annual_df["cumulative_return_pct"] = annual_df["annual_return_pct"].cumsum()
        fund_name = fund['name']
        all_funds_annual.append(fund_name)
        all_funds_annual.append(annual_df)
        # all_funds_annual.append(get_spy_cum_returns(startYear))

    for fund_perf in all_funds_annual:
        print("\n" + "=" * 80)
        print(fund_perf)