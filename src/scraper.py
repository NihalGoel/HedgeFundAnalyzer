import requests
import re
from bs4 import BeautifulSoup

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

    return all_holdings

def clean_historical_row(row):
    # Normalize quarter string
    quarter = re.sub(r"\s+", " ", row["quarter"]).strip()

    # Convert portfolio value to millions
    val_str = row["portfolio_value"].replace("$", "").strip()
    multiplier = 1000 if val_str.endswith("B") else 1
    value_num = float(re.sub(r"[MB]", "", val_str))

    return {
        "quarter": quarter,
        "portfolio_value_mil": round(value_num * multiplier, 2),
        "ticker": row["ticker"].strip(),
        "company": row["company"].strip(),
        "weight_pct": round(float(row["weight_pct"]), 2)
    }

def get_fund_holdings(filing_url, filing_date=None):
    resp = requests.get(filing_url, headers=headers)
    soup = BeautifulSoup(resp.content, "lxml")

    table = soup.find("table", id="grid")
    rows = table.find_all("tr")[1:]
    holdings = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 6:
            ticker = cols[1].get_text(strip=True).split()[0]
            weight = cols[2].get_text(strip=True)
            shares = cols[4].get_text(strip=True)
            reported_price = cols[5].get_text(strip=True)
            value = cols[6].get_text(strip=True)

            holdings.append({
                "ticker": ticker,
                "weight": weight,
                "shares": shares,
                "reported_price": reported_price,
                "value": value,
                "date": filing_date
            })

    return holdings

if __name__ == "__main__":
    funds = get_fund_urls()
    for fund in funds[:2]:  # Scrape first 2 funds for demo
        # print(f"Scraping holdings for {fund['name']}...")
        # holdings = get_fund_holdings(fund['url'])
        # print(holdings)
        raw_holdings = get_historical_holdings_matrix(fund['url'])
        cleaned_holdings = [clean_historical_row(h) for h in raw_holdings]
        print(cleaned_holdings)