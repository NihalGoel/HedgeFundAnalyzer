from dataroma.scraper import get_fund_urls
from dataroma.scraper import get_historical_holdings_matrix
from performance_calc.fund_performance import append_number_of_shares_to_holding

if __name__ == "__main__":
    funds = get_fund_urls()
    for fund in funds[:2]:  # Scrape first 2 funds for demo
        print(f"Scraping holdings for {fund['name']}...")
        holdings = get_historical_holdings_matrix(fund['url'])
        performance = append_number_of_shares_to_holding(holdings)
        # print(performance)