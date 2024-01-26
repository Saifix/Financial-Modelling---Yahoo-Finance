import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import scipy.stats as stats


def cal_portfolio_perf(combined_returns, Rf):
    # Calculate additional metrics
    portfolio_returns = combined_returns["Saif's Fund"]
    benchmark_returns = combined_returns['GSPC Monthly Return']

    portfolio_returns = portfolio_returns.fillna(0)
    benchmark_returns = benchmark_returns.fillna(0)

    # Check if there are NaN values after dropping them
    if portfolio_returns.isnull().any() or benchmark_returns.isnull().any():
        raise ValueError("NaN values are present in portfolio or benchmark returns after dropping.")

    # Calculate mean, std, min, max
    mean_return = portfolio_returns.mean()
    std_return = portfolio_returns.std()
    min_return = portfolio_returns.min()
    max_return = portfolio_returns.max()

    # Calculate Alpha, Beta, R-squared
    X = benchmark_returns.values.reshape(-1, 1)
    y = portfolio_returns.values

    # Check for NaN values in X and y
    if np.isnan(X).any() or np.isnan(y).any():
        raise ValueError("NaN values are present in X or y after dropping.")

    # Check if there are NaN values after dropping them
    if portfolio_returns.isnull().any() or benchmark_returns.isnull().any():
        raise ValueError("NaN values are present in portfolio or benchmark returns after dropping.")

    model = LinearRegression().fit(X, y)
    alpha = model.intercept_
    beta = model.coef_[0]
    r_squared = model.score(X, y)

    # Check if there are NaN values in the calculated metrics
    if np.isnan(alpha) or np.isnan(beta) or np.isnan(r_squared):
        raise ValueError("NaN values are present in calculated metrics.")

    # Calculate Sharpe ratio
    sharpe_ratio = (mean_return - Rf) / std_return

    # Calculate Treynor ratio
    treynor_ratio = (mean_return - Rf) / beta

    # Print the metrics
    print(f"Mean Return: {mean_return:.4f}")
    print(f"Standard Deviation (in %): {std_return * 100:.4f}")
    print(f"Minimum Return (in %): {min_return * 100:.4f}")
    print(f"Maximum Return (in %): {max_return * 100:.4f}")
    print(f"Alpha: {alpha:.4f}")
    print(f"Beta: {beta:.4f}")
    print(f"R-squared: {r_squared:.4f}")
    print(f"Sharpe Ratio: {sharpe_ratio:.4f}")
    print(f"Treynor Ratio: {treynor_ratio:.4f}")

    # Plot a histogram of portfolio returns with lines for Annesha Fund and GSPC
    plt.figure(figsize=(10, 6))

    # Plot histogram
    hist, bins, _ = plt.hist(portfolio_returns, bins=20, color='white', edgecolor='maroon', alpha=0.7,histtype='step', label="Annesha's Fund", density=True)
    plt.hist(benchmark_returns, bins=bins, color='white', edgecolor='blue', alpha=0.7, label='GSPC', density=True,histtype='step')

    plt.title('Histogram of Portfolio Returns')
    plt.xlabel('Monthly Returns')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(False)
    plt.show()