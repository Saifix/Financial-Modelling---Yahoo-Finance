
from Market_Cap import get_historical_data
import pandas as pd


def cal_liquidity(excel_file, company_names, constituents_data):

    sheet_name = "Liquidity_annual"
    # Check if the sheet already exists and remove it
    with pd.ExcelWriter(excel_file, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        # Create an empty list for liquidity data
        liquidity_data = []

        # Iterate through each year
        for year in range(2002, 2023):  # Adjusted the range to include 2022
            # Extract closing prices for the last trading day of each year

            # Iterate through each custom ticker
            for ticker in company_names:
                try:
                    stock_data = get_historical_data(
                        ticker, f"{year}-01-01", f"{year}-12-31")
                    if stock_data is not None:
                        daily_volume = stock_data["Volume"]
                        total_shares_outstanding = constituents_data.loc[
                            constituents_data["ticker"] == ticker, "Share_outstanding"].values[0]
                        liquidity = daily_volume.sum() / total_shares_outstanding

                        # Append a dictionary to the list
                        liquidity_data.append(
                            {"Ticker": ticker, "Liquidity": liquidity, "Year": year})
                    else:
                        pass
                        #print(f"No data available for {ticker} in {year}")
                except Exception as e:
                    pass
                    #print(f"Failed download for {ticker}: {e}")

            # Convert the list to a DataFrame
            liquidity_df = pd.DataFrame(liquidity_data)

            # Pivot the DataFrame to have years in the first column and tickers in the header row
            pivot_liquidity_df = liquidity_df.pivot(
                index='Year', columns='Ticker', values='Liquidity')

            # Save the pivoted liquidity data for the year in a new sheet
            pivot_liquidity_df.to_excel(
                writer, sheet_name=sheet_name, index=True, header=True)

    print("Liquidity data added to the Excel file.")
