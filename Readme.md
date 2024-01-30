# 📈 Stock Market Investment Project 📊


## Project Summary

I successfully completed the university assignment as a fund manager, reporting on the performance of a mutual fund with 25 assigned companies from the S&P 500 index. Below are the key tasks I performed:

### 1. Download Data
- Downloaded historical stock prices for all assigned companies from Yahoo Finance.
- Saved close and adjusted close prices, as well as volume, in separate sheets in an Excel file with sheet_names "Price_daily," "Adj_Price_daily," and "Volume_daily."
- Downloaded prices for the S&P 500 index (^GSPC) and saved them in a sheet named "S&P 500" in the same Excel file.

### 2. Calculate Firm Information
- Calculated the market capitalization of each firm per year.
- Calculated the sum of daily volume for each firm per year, divided by the total shares outstanding, and saved it in the sheet "Liquidity_annual."
- Computed annual, monthly, and daily returns using adjusted close prices and saved them in sheets labeled "Returns_annual," "Returns_monthly," and "Returns_daily."
- Calculated the standard deviation of each stock in each year using daily returns and saved them in a sheet called "Risk_annual."
- Provided summary statistics for portfolio holdings in the sheet "Firm_Summary_Stat."

### 3. Portfolio Analysis
- Constructed the portfolio based on the assigned fund strategy (Size, Liquidity, Return, Risk, Equal) from January 2003 to December 2022.
- Saved the monthly returns of the portfolio in the sheet "PortfolioReturn_monthly."
- Reported summary statistics of the portfolio and S&P 500 index return in the sheet "Fund_summary."
- Calculated and reported Alpha, Beta, R2, Sharpe ratio, and Treynor ratio with respect to the S&P 500 index.
- Reported industry composition in the sheet "Funds_Holdings_Composition."
- Plotted a pie chart showing the percentage investment in each firm at the end of the sample.
- Plotted a pie chart showing the percentage investment in each industry at the end of the sample.

### 4. Plot the Fund’s Performance
- Plotted histograms for the fund's return and S&P 500 index returns with 20 bins.
- Plotted the cumulative return of the portfolio and S&P 500 from January 2003 to December 2022.
- Plotted the annual return of the portfolio and S&P 500 using bar plots on the same graph.

I ensured that my code is self-explanatory, runs without errors, and provided detailed descriptions in each cell to facilitate understanding. I have also included external files, such as the Excel file with the results and any additional files needed for the code to run successfully.


## Features

- **Data Collection**: Utilized Yahoo Finance API to gather historical stock prices and other relevant financial data for S&P 500 companies.
- **Analysis and Visualization**: Conducted comprehensive analysis of the collected data, including price trends, volatility, and financial ratios.
- **Machine Learning Models**: Implemented machine learning models for predicting stock prices or identifying potential investment opportunities.
- **Portfolio Optimization**: Developed algorithms for optimizing investment portfolios based on risk tolerance and expected returns.

## Technologies Used

- Python 🐍
- Pandas 🐼
- NumPy 🔢
- Matplotlib 📊
- Scikit-learn 🧠
- Yahoo Finance API 💹


