import yfinance as yf
import pandas as pd

def get_historical_data(ticker_symbol, start_date, end_date):
    try:
        stock = yf.Ticker(ticker_symbol)
        data = stock.history(start=start_date, end=end_date)
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return None

def calculate_market_caps(company_names, constituents_data, startsdate, endsdate):
    # Create a DataFrame to store market caps
    market_caps = pd.DataFrame()

    # Iterate through each company
    for ticker in company_names:
        try:
            stock_data = get_historical_data(ticker, startsdate, endsdate)
            if stock_data is not None:
                closing_prices = stock_data["Close"]
                shares_outstanding = constituents_data.loc[constituents_data["ticker"] == ticker, "Share_outstanding"].values[0]
                market_cap = closing_prices * shares_outstanding
                market_caps[ticker] = market_cap
            else:
                print(f"No data available for {ticker} on {endsdate}")
        except yf.utils.exceptions.YfinanceError as e:
            print(f"Failed download for {ticker}: {e}")

    return market_caps
