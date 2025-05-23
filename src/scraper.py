import requests
from bs4 import BeautifulSoup


def get_fund_urls():
    url = "https://www.dataroma.com/m/home.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/113.0.0.0 Safari/537.36"
    }

    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, "lxml")

    fund_links = soup.select("a[href*='holdings.php?m=']")
    funds = [{"name": a.text.strip(), "url": f"https://www.dataroma.com{a['href']}"} for a in fund_links]
    return funds

def get_fund_holdings(fund_url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    resp = requests.get(fund_url, headers=headers)
    soup = BeautifulSoup(resp.content, "lxml")

    table = soup.find("table", {"class": "holdings"})
    rows = table.find_all("tr")[1:]  # skip header

    holdings = []
    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 10:
            continue  # skip malformed rows
        holdings.append({
            "ticker": cells[0].text.strip(),
            "company": cells[1].text.strip(),
            "percent_portfolio": cells[2].text.strip(),
            "reported_price": cells[6].text.strip(),
            "date_filed": cells[9].text.strip()
        })

    return holdings

if __name__ == "__main__":
    funds = get_fund_urls()
    for fund in funds[:5]:  # Scrape first 5 funds for demo
        print(f"Scraping holdings for {fund['name']}...")
        holdings = get_fund_holdings(fund['url'])
        print(holdings)