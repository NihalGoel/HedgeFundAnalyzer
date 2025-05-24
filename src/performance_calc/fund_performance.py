import pandas as pd

from collections import defaultdict

from stock_history.stock_ticker import get_average_price_per_quarter


def calculate_quarterly_pnl(holdings):
    """
    Calculates realized PnL for share reductions per quarter and ticker.
    holdings: list of dicts with 'quarter', 'ticker', 'number_of_shares', 'portfolio_value_mil'
    get_price_func: function(ticker, quarter_num, year) -> price
    Returns: list of dicts with keys: 'quarter', 'ticker', 'realized_pnl_mil', 'pnl_pct_of_portfolio'
    """
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
                quarter_str = current['quarter']
                year = int(quarter_str.split()[0])
                quarter_num = int(quarter_str.split()[1][1])
                sell_price = get_average_price_per_quarter(ticker, quarter_num, year)

                prev_quarter_str = prev_holding['quarter']
                prev_year = int(prev_quarter_str.split()[0])
                prev_quarter_num = int(prev_quarter_str.split()[1][1])
                cost_basis_price = get_average_price_per_quarter(ticker, prev_quarter_num, prev_year)

                if sell_price is None or cost_basis_price is None:
                    print(f"Skipping {ticker} for {quarter_str} due to missing price data.")
                    continue

                shares = prev_holding['number_of_shares']
                pnl = shares * (sell_price - cost_basis_price)
                portfolio_value = current['portfolio_value_mil'] * 1_000_000
                pnl_pct = pnl / portfolio_value if portfolio_value else 0.0

                pnl_results.append({
                    'quarter': current['quarter'],
                    'ticker': ticker,
                    'pnl_mil': pnl / 1_000_000,
                    'pnl_pct_of_portfolio': pnl_pct * 100,
                    'portfolio_value_mil': current['portfolio_value_mil']
                })
            prev_holding = current
    return pnl_results

def calculate_annual_pnl(holdings):
    pnl_results = calculate_quarterly_pnl(holdings)
    df = pd.DataFrame(pnl_results)
    df['year'] = df['quarter'].str.extract(r'(\d{4})').astype(int)

    # Total realized PnL per year
    total_pnl = df.groupby('year')['pnl_mil'].sum().reset_index(name='total_pnl_mil')

    # avg portfolio value used in return calculation
    avg_portfolio_value = df.groupby('year')['portfolio_value_mil'].mean().reset_index(name='avg_portfolio_value_mil')

    # Merge and calculate percentage return
    merged = total_pnl.merge(avg_portfolio_value, on='year')
    merged['annual_return_pct'] = (merged['total_pnl_mil'] / merged['avg_portfolio_value_mil']) * 100

    return merged