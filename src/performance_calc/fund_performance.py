import pandas as pd

from collections import defaultdict
from stock_history.stock_ticker import get_average_price_per_quarter

def get_share_amount(holding, ticker_price):
    portfolio_value_mil = holding['portfolio_value_mil']
    weight_pct = holding['weight_pct']

    holding_value_mil = portfolio_value_mil * weight_pct / 100
    number_of_shares = holding_value_mil * 1_000_000 / ticker_price
    return int(round(number_of_shares))

def append_number_of_shares_to_holding(holdings):
    valid_holdings = []

    for holding in holdings:
        ticker = holding['ticker']
        quarter_str = holding['quarter']
        year = int(quarter_str.split()[0])
        if year < 2024:
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


def calculate_quarterly_realized_pnl(holdings):
    """
    Calculates realized PnL for share reductions per quarter and ticker.
    holdings: list of dicts with 'quarter', 'ticker', 'number_of_shares', 'portfolio_value_mil'
    get_price_func: function(ticker, quarter_num, year) -> price
    Returns: list of dicts with keys: 'quarter', 'ticker', 'realized_pnl_mil', 'pnl_pct_of_portfolio'
    """
    holdings = append_number_of_shares_to_holding(holdings)

    holdings_by_ticker = defaultdict(list)
    for h in holdings:
        holdings_by_ticker[h['ticker']].append(h)

    pnl_results = []

    for ticker, ticker_holdings in holdings_by_ticker.items():
        # Sort by quarter (assumes format 'YYYY Qn')
        ticker_holdings.sort(key=lambda x: (int(x['quarter'].split()[0]), int(x['quarter'].split()[1][1])))
        prev_holding = None
        for current in ticker_holdings:
            if prev_holding:
                shares_diff = prev_holding['number_of_shares'] - current['number_of_shares']
                if shares_diff > 0:
                    # Realized sale
                    # Sell price is next quarter's average price
                    quarter_str = current['quarter']
                    year = int(quarter_str.split()[0])
                    quarter_num = int(quarter_str.split()[1][1])
                    sell_price = get_average_price_per_quarter(ticker, quarter_num, year)
                    # Cost basis: use previous quarter's price for the shares sold
                    prev_quarter_str = prev_holding['quarter']
                    prev_year = int(prev_quarter_str.split()[0])
                    prev_quarter_num = int(prev_quarter_str.split()[1][1])
                    cost_basis_price = get_average_price_per_quarter(ticker, prev_quarter_num, prev_year)
                    pnl = shares_diff * (sell_price - cost_basis_price)
                    portfolio_value = current['portfolio_value_mil'] * 1_000_000
                    pnl_pct = pnl / portfolio_value if portfolio_value else 0.0
                    pnl_results.append({
                        'quarter': current['quarter'],
                        'ticker': ticker,
                        'realized_pnl_mil': pnl / 1_000_000,
                        'pnl_pct_of_portfolio': pnl_pct * 100,
                        'portfolio_value_mil': current['portfolio_value_mil']
                    })
            prev_holding = current
    return pnl_results

def calculate_annual_pnl(pnl_results):
    df = pd.DataFrame(pnl_results)
    df['year'] = df['quarter'].str.extract(r'(\d{4})').astype(int)

    # Total realized PnL per year
    total_pnl = df.groupby('year')['realized_pnl_mil'].sum().reset_index(name='total_realized_pnl_mil')

    # avg portfolio value used in return calculation
    avg_portfolio_value = df.groupby('year')['portfolio_value_mil'].mean().reset_index(name='avg_portfolio_value_mil')

    # Merge and calculate percentage return
    merged = total_pnl.merge(avg_portfolio_value, on='year')
    merged['annual_return_pct'] = (merged['total_realized_pnl_mil'] / merged['avg_portfolio_value_mil']) * 100

    return merged