import requests
from bs4 import BeautifulSoup
from dataroma.cleaner import clean_historical_row
from runner.config import startYear
from stock_history.stock_ticker import get_average_price_per_quarter

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/113.0.0.0 Safari/537.36"
}


def get_fund_urls():
    url = "https://www.dataroma.com/m/home.php"

    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, "lxml")

    fund_links = soup.select("a[href*='holdings.php?m=']")
    funds = [{"name": a.text.strip(), "url": f"https://www.dataroma.com{a['href']}"} for a in fund_links]
    return funds

def get_historical_holdings_matrix(fund_url):
    fund_id = fund_url.split("m=")[-1]
    url = f"https://www.dataroma.com/m/hist/p_hist.php?f={fund_id}"
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, "lxml")

    rows = soup.select("table#grid tr")[1:]  # Skip header
    all_holdings = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 3:
            continue

        quarter = cols[0].text.strip().replace('\xa0', ' ')
        quarter = quarter.replace("\xa0", " ").replace("&nbsp", " ").strip()
        port_value = cols[1].text.strip()

        for sym_cell in cols[2:]:
            link = sym_cell.find("a")
            tooltip = sym_cell.find("div")

            if not link or not tooltip:
                continue

            ticker = link.text.strip()
            info_lines = tooltip.get_text(separator="\n").strip().split("\n")
            company = info_lines[0]
            pct = info_lines[1].replace("% of portfolio", "").strip()

            all_holdings.append({
                "quarter": quarter,
                "portfolio_value": port_value,
                "ticker": ticker,
                "company": company,
                "weight_pct": float(pct)
            })

    holdings = [clean_historical_row(h) for h in all_holdings]
    holdings = append_number_of_shares_to_holding(holdings)
    return holdings

def append_number_of_shares_to_holding(holdings):
    valid_holdings = []

    for holding in holdings:
        ticker = holding['ticker']
        quarter_str = holding['quarter']
        year = int(quarter_str.split()[0])
        if year < startYear:
            continue
        quarter_num = int(quarter_str.split()[1][1])  # 'Q4' -> 4

        ticker_price = get_average_price_per_quarter(ticker, quarter_num, year)
        if ticker_price is None:
            print(f"Skipping {ticker} for {quarter_str} — no price data.")
            continue

        number_of_shares = get_share_amount(holding, ticker_price)
        holding['number_of_shares'] = number_of_shares

        valid_holdings.append(holding)

    return valid_holdings

def get_share_amount(holding, ticker_price):
    portfolio_value_mil = holding['portfolio_value_mil']
    weight_pct = holding['weight_pct']

    holding_value_mil = portfolio_value_mil * weight_pct / 100
    number_of_shares = holding_value_mil * 1_000_000 / ticker_price
    return int(round(number_of_shares))
