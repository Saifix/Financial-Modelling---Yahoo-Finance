import pandas as pd


def calculate_returns(prices):
    return prices.pct_change()


def cal_returns(excel_file, company_names, data):
    # Create a new Excel file or open existing file
    with pd.ExcelWriter(excel_file, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        for data_type in ["Adj_Price_daily"]:
            # Create an empty DataFrame to store combined data for all companies
            combined_data = pd.DataFrame()

            for ticker in company_names:
                #print(f"Downloading {data_type} for {ticker}...")
                #data = download_data(ticker, start_date, end_date)

                # Extract relevant column for the current data type
                if data_type == "Adj_Price_daily":
                    current_data = data["Adj Close"]

                # Combine data for all tickers
                combined_data[ticker] = current_data

            # Write combined data to a single sheet
            combined_data.to_excel(writer, sheet_name=data_type)

            # Calculate returns
            returns_daily = calculate_returns(combined_data)
            returns_monthly = calculate_returns(
                combined_data.resample('M').last())
            returns_annual = calculate_returns(
                combined_data.resample('A').last())

            # Append returns to existing or new sheets
            returns_daily.to_excel(
                writer, sheet_name="Returns_daily", index=True, header=True)
            returns_monthly.to_excel(
                writer, sheet_name="Returns_monthly", index=True, header=True)
            returns_annual.to_excel(
                writer, sheet_name="Returns_annual", index=True, header=True)

    print("Data download, Excel file update, and returns calculation completed.")
