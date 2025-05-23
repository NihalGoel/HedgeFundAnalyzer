from dataroma.scraper import get_fund_urls
from dataroma.scraper import get_historical_holdings_matrix
from performance_calc.fund_performance import *

if __name__ == "__main__":
    funds = get_fund_urls()
    for fund in funds[:1]:  # Scrape first 2 funds for demo
        print(f"Scraping holdings for {fund['name']}...")
        holdings = get_historical_holdings_matrix(fund['url'])
        # performance = append_number_of_shares_to_holding(holdings)
        pnl_results = calculate_quarterly_realized_pnl(holdings)
        aggregate_pnl = calculate_annual_pnl(pnl_results)
        print(aggregate_pnl)