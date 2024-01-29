import numpy as np
import pandas as pd
import yfinance as yf
import scipy.optimize as opt
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
from pandas.tseries.offsets import MonthEnd


def SharpeRatio(weights, Ret, Rf):
    w = np.append(weights, 1 - sum(weights))
    Ret_portfolio = (w * Ret).sum(axis=1)
    SR_portfolio = -1 * (Ret_portfolio.mean() - Rf) * \
        12 / Ret_portfolio.std() / np.sqrt(12)
    return SR_portfolio


start_date = '2003-01-01'
end_date = '2022-12-31'


def cal_portfolio(tickers, output_file_path):
    panel_data = yf.download(tickers, start_date, end_date)

    # Resample data to monthly frequency and fill missing data with zeros
    Returns = panel_data['Adj Close'].resample(
        "1m").ffill().pct_change().fillna(0)

    FF_3Factor_All = pdr.get_data_famafrench(
        'F-F_Research_Data_Factors', start_date, end_date)
    FF_3Factor = FF_3Factor_All[0] / 100
    FF_3Factor.index = FF_3Factor.index.to_timestamp() + MonthEnd(1)
    FF_3Factor = FF_3Factor[1:]
    Rf = FF_3Factor['RF'].mean()

    weights_0 = np.ones(len(tickers) - 1) / len(tickers)
    optimal_weights = opt.fmin_bfgs(
        SharpeRatio, weights_0, args=(Returns[tickers], Rf))

    optimal_weights_all = np.append(optimal_weights, 1 - sum(optimal_weights))
    optimal_weights_all = pd.Series(optimal_weights_all, index=tickers)
    optimal_SharpeRatio = -1 * \
        SharpeRatio(optimal_weights, Returns[tickers], Rf)

    # Code for the second part
    # Define the ticker symbol for S&P 500 (^GSPC)
    ticker_symbol = "^GSPC"

    # Download historical data
    data_gspc = yf.download(ticker_symbol, start=start_date, end=end_date)

    # Resample data to get monthly returns
    monthly_returns_gspc = data_gspc['Adj Close'].resample(
        'M').ffill().pct_change()

    # Combine Saif's Fund and GSPC Monthly Return
    combined_returns = pd.DataFrame({
        'Date': Returns.index.strftime('%Y-%m'),
        "Saif's Fund": (Returns[tickers] * optimal_weights_all).sum(axis=1).round(3),
        'GSPC Monthly Return': monthly_returns_gspc.round(3),
        'Year': Returns.index.year
    })

    # Reset the index before creating cumulative returns
    combined_returns.reset_index(drop=True, inplace=True)

    # Plot for annual returns as a bar chart
    annual_returns = combined_returns.groupby('Year').agg(
        {'Saif\'s Fund': 'sum', 'GSPC Monthly Return': 'sum'})

    plt.figure(figsize=(10, 6))

    # Bar chart for annual returns
    bar_width = 0.35
    plt.bar(annual_returns.index - bar_width/2,
            annual_returns["Saif's Fund"], bar_width, label="Saif's Fund")
    plt.bar(annual_returns.index + bar_width/2,
            annual_returns['GSPC Monthly Return'], bar_width, label='GSPC')

    plt.title('Annual Returns')
    plt.xlabel('Year')
    plt.ylabel('Returns')
    plt.legend()
    plt.grid(True)

    # Save the bar chart as an image
    bar_chart_image_path = 'bar_chart.png'
    plt.savefig(bar_chart_image_path)
    plt.close()

    # Create a cumulative returns DataFrame
    cumulative_returns = combined_returns.copy()
    cumulative_returns['Cumulative Saif\'s Fund'] = cumulative_returns["Saif's Fund"].cumsum()
    cumulative_returns['Cumulative GSPC'] = cumulative_returns['GSPC Monthly Return'].cumsum()

    # Plot for cumulative returns as a step plot
    plt.figure(figsize=(10, 6))

    # Line chart for cumulative returns
    plt.step(cumulative_returns.index,
             cumulative_returns["Cumulative Saif's Fund"], label="Cumulative Saif's Fund", where='post')
    plt.step(cumulative_returns.index,
             cumulative_returns['Cumulative GSPC'], label='Cumulative GSPC', where='post')

    plt.title('Cumulative Returns')
    plt.xlabel('Month')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.grid(True)

    # Save the cumulative returns chart as an image
    cumulative_chart_image_path = 'cumulative_chart.png'
    plt.savefig(cumulative_chart_image_path)
    plt.close()

    # Save the output to an existing Excel file with the plots
    output_file_path = 'Stock Data Output.xlsx'
    with pd.ExcelWriter(output_file_path, engine='openpyxl', mode='a', if_sheet_exists="replace") as writer:
        # Save the combined returns to the sheet "PortfolioReturn_monthly"
        combined_returns.to_excel(
            writer, index=False, sheet_name='PortfolioReturn_monthly')

        # Save the bar chart image to the same worksheet
        worksheet_bar_chart = writer.sheets['PortfolioReturn_monthly']
        image_width = 400
        image_height = 300
        # worksheet_bar_chart.insert_image('F2', bar_chart_image_path, {'x_scale': image_width / 100, 'y_scale': image_height / 100})

        # Save the cumulative returns chart image to the same worksheet
        worksheet_cumulative_chart = writer.sheets['PortfolioReturn_monthly']
        # worksheet_cumulative_chart.insert_image('M2', cumulative_chart_image_path, {'x_scale': image_width / 100, 'y_scale': image_height / 100})

    print(f'Output saved to {output_file_path}')

    return combined_returns, Rf
