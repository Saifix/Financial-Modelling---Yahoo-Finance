import pandas as pd
import numpy as np
import yfinance as yf

def calculate_beta(data, benchmark, start_date, end_date):
    # Download historical stock prices
    monthly_data = data.resample('M').last()
    stock_data = monthly_data.loc[start_date:end_date]
    #stock_data = yf.download(stock_symbol, start=start_date, end=end_date, interval='1mo')
    #benchmark_data = yf.download(benchmark_symbol, start=start_date, end=end_date, interval='1mo')
    monthly_b_data = benchmark.resample('M').last()
    benchmark_data = monthly_b_data.loc[start_date:end_date]
    # Extract adjusted closing prices
    stock_adj_close = stock_data['Adj Close']
    benchmark_adj_close = benchmark_data['Adj Close']

    # Calculate monthly returns
    stock_returns = stock_adj_close.pct_change().dropna()
    benchmark_returns = benchmark_adj_close.pct_change().dropna()

    # Calculate covariance and variance
    covariance = np.cov(stock_returns, benchmark_returns)[0, 1]
    variance = np.var(benchmark_returns)

    # Calculate beta
    beta = covariance / variance

    return beta

def cal_beta_main(tickers,data,benchmark_data,start_date,end_date,constituents_file,Output_file,summary_stats_df):
    # Benchmark symbol (e.g., S&P 500)


    # Store beta values calculated from download in a dictionary
    downloaded_betas = {}
    for stock_symbol in tickers:
        beta_value = calculate_beta(data, benchmark_data, start_date, end_date)
        downloaded_betas[stock_symbol] = beta_value

    # Replace 'your_tickers_list' with your list of tickers
    given_tickers = tickers


    # Read the Excel file
    excel_data = pd.ExcelFile(constituents_file)

    # Get the required sheet
    sheet_name = 'S&P 500 Constituent'
    sheet_data = excel_data.parse(sheet_name)

    # Get the column 'Market Beta on Nov 2023'
    market_beta_column = 'Market Beta on Nov 2023'

    # Filter rows based on the given tickers
    filtered_rows = sheet_data[sheet_data['ticker'].isin(given_tickers)]

    # Display the 'Ticker' and 'Market Beta on Nov 2023' columns for the filtered rows
    for index, row in filtered_rows.iterrows():
        ticker = row['ticker']
        excel_beta = row[market_beta_column]

        # Check if the ticker has a downloaded beta value
        if ticker in downloaded_betas:
            downloaded_beta = downloaded_betas[ticker]

            if (downloaded_beta > excel_beta):
                percentage_difference = (
                    (downloaded_beta - excel_beta) / max(abs(excel_beta), abs(downloaded_beta))) * 100
            elif (excel_beta > downloaded_beta):
                percentage_difference = (
                    (excel_beta - downloaded_beta) / max(abs(excel_beta), abs(downloaded_beta))) * 100

            # Calculate the difference in percentage

            # Update the "Firm_Summary_Stat" sheet with Excel Beta, Downloaded Beta, and Percentage Difference
            with pd.ExcelWriter(Output_file, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                summary_stats_df.at[ticker, 'Excel Beta'] = excel_beta
                summary_stats_df.at[ticker, 'Downloaded Beta'] = downloaded_beta
                summary_stats_df.at[ticker,
                                    'Percentage Difference'] = percentage_difference
                summary_stats_df.T.to_excel(
                    writer, sheet_name="Firm_Summary_Stat", index=True, header=True)

            # Print the results
            # print(f"Ticker: {ticker}, Downloaded Beta: {downloaded_beta}, Excel Beta: {excel_beta}, Difference (%): {percentage_difference}")
        else:
            print(f"Ticker: {ticker}, Downloaded Beta not available")