import requests
from bs4 import BeautifulSoup

from dataroma.config import headers
from runner.config import minAddedAmount, minPercentageOfPortfolio


def get_latest_quarter_buys(fund_url):

    resp = requests.get(fund_url, headers=headers)
    soup = BeautifulSoup(resp.content, "lxml")

    table = soup.find("table", id="grid")
    rows = table.find_all("tr")[1:]  # Skip the header row

    latest_quarter_buys = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 12:
            continue

        stock = {
            "ticker": cols[1].find("a").text.strip(),
            "company": cols[1].find("span").text.strip() if cols[1].find("span") else "",
            "percentage": cols[2].text.strip(),
            "activity": cols[3].text.strip(),
            # "shares": cols[4].text.strip(),
            # "reported_price": cols[5].text.strip(),
            "value": cols[6].text.strip(),
            # "current_price": cols[8].text.strip(),
            # "price_change_pct": cols[9].text.strip(),
            # "52_week_low": cols[10].text.strip(),
            # "52_week_high": cols[11].text.strip()
        }

        latest_quarter_buys.append(stock)

    buy_activities = []
    for stock in latest_quarter_buys:
        activity = stock["activity"].lower()
        try:
            portfolio_percent = float(stock["percentage"])
            if "add" in activity:
                activity_percent = float(activity.split()[-1].replace("%", ""))
                if activity_percent >= minAddedAmount and portfolio_percent >= minPercentageOfPortfolio:
                    buy_activities.append(stock)
            elif "buy" in activity and portfolio_percent >= minPercentageOfPortfolio:
                buy_activities.append(stock)
        except (ValueError, IndexError):
            continue

    return buy_activities
