import requests
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

def get_fund_holdings(fund_url):
    resp = requests.get(fund_url, headers=headers)
    soup = BeautifulSoup(resp.content, "lxml")

    table = soup.find("table", id="grid")
    rows = table.find_all("tr")[1:]  # Skip the header row
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 3:
            ticker = cols[1].get_text(strip=True).split()[0]  # Get ticker only (before dash)
            weight = cols[2].get_text(strip=True)
            print(ticker, weight)

if __name__ == "__main__":
    funds = get_fund_urls()
    for fund in funds[:5]:  # Scrape first 5 funds for demo
        print(f"Scraping holdings for {fund['name']}...")
        holdings = get_fund_holdings(fund['url'])
        print(holdings)