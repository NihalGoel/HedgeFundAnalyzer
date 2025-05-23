import requests
from bs4 import BeautifulSoup
from config import headers
from cleaner import clean_historical_row


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

    return all_holdings


if __name__ == "__main__":
    funds = get_fund_urls()
    for fund in funds[:2]:  # Scrape first 2 funds for demo
        # print(f"Scraping holdings for {fund['name']}...")
        raw_holdings = get_historical_holdings_matrix(fund['url'])
        cleaned_holdings = [clean_historical_row(h) for h in raw_holdings]
        print(cleaned_holdings)