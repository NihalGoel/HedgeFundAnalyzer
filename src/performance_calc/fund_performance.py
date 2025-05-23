from stock_history_nyse.stock_ticker import get_average_price_per_quarter

def get_share_amount(holding, ticker_price):
    portfolio_value_mil = holding['portfolio_value_mil']
    weight_pct = holding['weight_pct']

    holding_value_mil = portfolio_value_mil * weight_pct / 100
    number_of_shares = holding_value_mil * 1_000_000 / ticker_price
    return int(round(number_of_shares))

def append_number_of_shares_to_holding(holdings):
    for holding in holdings:
        ticker = holding['ticker']
        quarter_str = holding['quarter']
        year = int(quarter_str.split()[0])
        quarter_num = int(quarter_str.split()[1][1])  # 'Q4' -> 4
        ticker_price = get_average_price_per_quarter(ticker, quarter_num, year)
        number_of_shares = get_share_amount(holding, ticker_price)
        holding['number_of_shares'] = number_of_shares

        print(f"Ticker: {ticker}, Year: {year}, Quarter: Q{quarter_num}, Number Of Shares: {number_of_shares}")
        # print(holding)
        print("-"*100)

    # print(holdings)
    return holdings