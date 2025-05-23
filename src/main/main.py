from dataroma.scraper import get_fund_urls
from dataroma.scraper import get_historical_holdings_matrix
from performance_calc.fund_performance import *

if __name__ == "__main__":
    funds = get_fund_urls()
    all_funds_annual = []
    for fund in funds[:1]:  # Scrape first 2 funds for demo
        print(f"Scraping holdings for {fund['name']}...")
        holdings = get_historical_holdings_matrix(fund['url'])
        # performance = append_number_of_shares_to_holding(holdings)
        pnl_results = calculate_quarterly_pnl(holdings)
        annual_df = calculate_annual_pnl(pnl_results)
        fund_name = fund['name']
        all_funds_annual.append(fund_name)
        all_funds_annual.append(annual_df)

    for fund_perf in all_funds_annual:
        print("\n" + "=" * 80)
        print(fund_perf)