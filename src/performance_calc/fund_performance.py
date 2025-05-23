from dataroma.scraper import *

if __name__ == "__main__":
    funds = get_fund_urls()
    for fund in funds[:2]:  # Scrape first 2 funds for demo
        # print(f"Scraping holdings for {fund['name']}...")
        raw_holdings = get_historical_holdings_matrix(fund['url'])
        cleaned_holdings = [clean_historical_row(h) for h in raw_holdings]
        print(cleaned_holdings)