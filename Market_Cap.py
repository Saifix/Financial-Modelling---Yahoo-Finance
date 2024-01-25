import pandas as pd
import yfinance as yf


def get_historical_data(ticker_symbol, start_date, end_date):
    try:
        stock = yf.Ticker(ticker_symbol)
        data = stock.history(start=start_date, end=end_date)
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return None


def cal_market_cap(startsdate, endsdate, constituents_file, output_file, tickers):

    constituents_data = pd.read_excel(
        constituents_file, sheet_name="S&P 500 Constituent")
    constituents_data = constituents_data[[
        "ticker", "Name", "Share_outstanding"]]

    # Create a new sheet for market capitalization
    with pd.ExcelWriter(output_file, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        # Iterate through each year
        for year in range(2002, 2022):
            # Extract closing prices for the last trading day of each year
            market_caps = pd.DataFrame()
            dates = None
            for ticker in tickers:
                try:
                    stock_data = get_historical_data(
                        ticker, startsdate, endsdate)
                    if stock_data is not None:
                        closing_prices = stock_data["Close"]
                        shares_outstanding = constituents_data.loc[constituents_data["ticker"]
                                                                   == ticker, "Share_outstanding"].values[0]
                        market_cap = closing_prices * shares_outstanding
                        market_caps[ticker] = market_cap
                        dates = stock_data.index
                    else:
                        print(
                            f"No data available for {ticker} on {year}-12-31")
                except Exception as e:
                    print(f"Failed download for {ticker}: {e}")

            # If market_caps is empty, continue to the next year
            if market_caps.empty:
                continue

            # Add a column for the year
            market_caps.insert(0, "Date", dates.strftime("%d-%m-%Y"))

            # Save the market caps for the year in a new sheet
            market_caps.to_excel(
                writer, sheet_name=f"Market_Caps", index=False)

    print("Market capitalization data added to the Excel file.")


def filter_last_date_per_year(file_path, sheet_name):
    # Read the Excel file
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    # Convert the date column to datetime type with the correct format
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce').dt.date

    # Extract the year from the date
    df['Year'] = pd.to_datetime(df['Date']).dt.year

    # Find the last date for each year
    last_dates_per_year = df.groupby('Year')['Date'].max().reset_index()

    # Merge with the original dataframe to keep only the last dates
    result_df = pd.merge(last_dates_per_year, df, on=['Year', 'Date'], how='inner')

    # Drop the Year column if you don't want to keep it in the final result
    result_df = result_df.drop(columns='Year')
    print(result_df)

    return result_df


