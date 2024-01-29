import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as opt
import yfinance as yf

# Function to calculate Sharpe Ratio
def SharpeRatio(weights, Ret, Rf):
    w = np.append(weights, 1 - sum(weights))
    Ret_portfolio = (w * Ret).sum(axis=1)
    SR_portfolio = -1 * (Ret_portfolio.mean() - Rf) * 12 / Ret_portfolio.std() / np.sqrt(12)
    return SR_portfolio



def cal_invest_sum(tickers, Rf, panel_data, excel_file_path,Output_file ):
    # Define the tickers and other parameters
    start_date = '2003-01-01'
    end_date = '2023-11-30'  # Updated end date

    # Download data
    panel_data = yf.download(tickers, start_date, end_date)

    # Resample data to monthly frequency and fill missing data with zeros
    Returns = panel_data['Adj Close'].resample("1m").ffill().pct_change().fillna(0)

    # Set initial weights
    weights_0 = np.ones(len(tickers) - 1) / len(tickers)

    # Optimize weights to maximize Sharpe Ratio
    optimal_weights = opt.fmin_bfgs(SharpeRatio, weights_0, args=(Returns[tickers], Rf))

    # Calculate final weights with cash
    optimal_weights_all = np.append(optimal_weights, 1 - sum(optimal_weights))
    optimal_weights_all = pd.Series(optimal_weights_all, index=tickers)

    # Calculate investments in each firm at the end of the sample
    investments = panel_data['Adj Close'].iloc[-1] * optimal_weights_all

    # Ensure that investments are non-negative
    investments[investments < 0] = 0

    # Calculate percentage investments
    percentage_investments = (investments / investments.sum()) * 100

    # Preserve the original order of tickers
    percentage_investments = percentage_investments.loc[tickers]

    # Display investments
    print("Investments at the end of the sample:")
    print(percentage_investments.round(2))

    # Save the summary data to Excel

    # Create a DataFrame to store the results
    summary_data = pd.DataFrame({'Symbols': tickers, end_date: percentage_investments.round(2)})
    # Append the summary_data to the 'fund_summary2' sheet in the Excel file
    with pd.ExcelWriter(Output_file, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        summary_data.to_excel(writer, sheet_name='fund_summary2', index=False)

    # Load industry data from Excel
    industry_data = pd.read_excel(excel_file_path, sheet_name='S&P 500 Constituent', usecols=['ticker', 'GICS Sector'])

    # Merge industry data with summary_data
    summary_data = pd.merge(summary_data, industry_data, left_on='Symbols', right_on='ticker', how='left')

    # Group by industry and sum investments
    industry_investments = summary_data.groupby('GICS Sector')[end_date].sum()

    # Plot a pie chart with leader lines for industries
    fig, ax = plt.subplots(figsize=(12, 8))
    wedges, texts, autotexts = ax.pie(industry_investments, autopct='%1.1f%%', textprops=dict(color="w"))

    # Add leader lines
    for i, text in enumerate(texts):
        angle = (wedges[i].theta2 - wedges[i].theta1) / 2. + wedges[i].theta1
        x = np.cos(np.radians(angle))
        y = np.sin(np.radians(angle))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={angle}"
        ax.annotate(f'{industry_investments.index[i]}', xy=(x, y), xytext=(1.35 * np.sign(x), 1.4 * y),
                    horizontalalignment=horizontalalignment, arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color='black'))

    plt.title('Industry Composition at the End of the Sample')
    plt.savefig('industry_pie_chart.png')
    plt.show()
