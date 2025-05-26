import requests
from bs4 import BeautifulSoup
from dataroma.config import headers

def get_fund_urls():
    url = "https://www.dataroma.com/m/home.php"

    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, "lxml")

    fund_links = soup.select("a[href*='holdings.php?m=']")
    funds = [{"name": a.text.strip(), "url": f"https://www.dataroma.com{a['href']}"} for a in fund_links]
    return funds