

def cal_portfolio_return(combined_returns, Rf):
    # Calculate additional metrics
    portfolio_returns = combined_returns["Saif's Fund"]
    benchmark_returns = combined_returns['GSPC Monthly Return']

    portfolio_returns = portfolio_returns.fillna(0)
    benchmark_returns = benchmark_returns.fillna(0)

    # Check if there are NaN values after dropping them
    if portfolio_returns.isnull().any() or benchmark_returns.isnull().any():
        raise ValueError("NaN values are present in portfolio or benchmark returns after dropping.")

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression

    # Calculate additional metrics
    portfolio_returns = combined_returns["Saif's Fund"]
    benchmark_returns = combined_returns['GSPC Monthly Return']

    portfolio_returns = portfolio_returns.fillna(0)
    benchmark_returns = benchmark_returns.fillna(0)

    # Check if there are NaN values after dropping them
    if portfolio_returns.isnull().any() or benchmark_returns.isnull().any():
        raise ValueError("NaN values are present in portfolio or benchmark returns after dropping.")

    # Calculate mean, std, min, max in annual percentage rates
    mean_return_annual = (1 + portfolio_returns).prod() ** (12 / len(portfolio_returns.index)) - 1
    std_return_annual = portfolio_returns.std() * np.sqrt(12)
    min_return_annual = portfolio_returns.min() * 12
    max_return_annual = portfolio_returns.max() * 12

    # Convert to percentage for display
    mean_return_annual_percent = mean_return_annual * 100
    std_return_annual_percent = std_return_annual * 100
    min_return_annual_percent = min_return_annual * 100
    max_return_annual_percent = max_return_annual * 100

    # Calculate Alpha, Beta, R-squared for Saif Fund
    X_portfolio = benchmark_returns.values.reshape(-1, 1)
    y_portfolio = portfolio_returns.values

    # Check for NaN values in X and y
    if np.isnan(X_portfolio).any() or np.isnan(y_portfolio).any():
        raise ValueError("NaN values are present in X or y for Saif Fund after dropping.")

    # Check if there are NaN values after dropping them
    if portfolio_returns.isnull().any() or benchmark_returns.isnull().any():
        raise ValueError("NaN values are present in Saif Fund or benchmark returns after dropping.")

    model_portfolio = LinearRegression().fit(X_portfolio, y_portfolio)
    alpha_portfolio = model_portfolio.intercept_
    beta_portfolio = model_portfolio.coef_[0]
    r_squared_portfolio = model_portfolio.score(X_portfolio, y_portfolio)

    # Calculate Sharpe ratio and Treynor ratio for Saif Fund
    sharpe_ratio_portfolio = (mean_return_annual - Rf) / std_return_annual
    treynor_ratio_portfolio = (mean_return_annual - Rf) / beta_portfolio

    # Calculate Alpha, Beta, R-squared for GSPC
    X_gspc = benchmark_returns.values.reshape(-1, 1)
    y_gspc = benchmark_returns.values

    # Check for NaN values in X and y
    if np.isnan(X_gspc).any() or np.isnan(y_gspc).any():
        raise ValueError("NaN values are present in X or y for GSPC after dropping.")

    model_gspc = LinearRegression().fit(X_gspc, y_gspc)
    alpha_gspc = model_gspc.intercept_
    beta_gspc = model_gspc.coef_[0]
    r_squared_gspc = model_gspc.score(X_gspc, y_gspc)

    # Calculate Sharpe ratio and Treynor ratio for GSPC
    sharpe_ratio_gspc = (benchmark_returns.mean() * 12 - Rf) / (benchmark_returns.std() * np.sqrt(12))
    treynor_ratio_gspc = (benchmark_returns.mean() * 12 - Rf) / beta_gspc

    # Create a DataFrame to store the results
    summary_data = pd.DataFrame({
        'Variable': ['Average', 'Standard Deviation', 'Minimum', 'Maximum', 'Alpha', 'Beta', 'R-squared', 'Sharpe Ratio', 'Treynor Ratio'],
        "Saif Fund": [f'{mean_return_annual_percent:.2f}%', f'{std_return_annual_percent:.2f}%', f'{min_return_annual_percent:.2f}%', f'{max_return_annual_percent:.2f}%', alpha_portfolio, beta_portfolio, r_squared_portfolio, sharpe_ratio_portfolio, treynor_ratio_portfolio],
        'GSPC': [f'{benchmark_returns.mean() * 12 * 100:.2f}%', f'{benchmark_returns.std() * np.sqrt(12) * 100:.2f}%', f'{benchmark_returns.min() * 12 * 100:.2f}%', f'{benchmark_returns.max() * 12 * 100:.2f}%', alpha_gspc, beta_gspc, r_squared_gspc, sharpe_ratio_gspc, treynor_ratio_gspc]
    })

    # Save the summary data to Excel
    excel_file_path = 'Stock Data Output.xlsx'
    with pd.ExcelWriter(excel_file_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        summary_data.to_excel(writer, sheet_name='Fund_summary', index=False)

    # Plot a histogram of portfolio returns with lines for Saif Fund and GSPC
    plt.figure(figsize=(10, 6))

    # Plot histogram
    hist, bins, _ = plt.hist(portfolio_returns, bins=20, color='white', edgecolor='maroon', alpha=0.7, histtype='step', label="Saif Fund", density=True)
    plt.hist(benchmark_returns, bins=bins, color='white', edgecolor='blue', alpha=0.7, label='GSPC', density=True, histtype='step')

    plt.title('Histogram of Portfolio Returns')
    plt.xlabel('Monthly Returns')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(False)
    plt.savefig('Histogram_Portfolio_Returns.png')
    plt.show()

