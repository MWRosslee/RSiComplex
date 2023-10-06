import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.model_selection import ParameterGrid


# Define your trading strategy rules
def implement_strategy(data, rsi_period, sma_period):
    data['RSI'] = 100 - (100 / (1 + (data['Close'].diff(1).fillna(0).rolling(window=rsi_period).apply(lambda x: sum(x[x < 0]), raw=True) /
                                 data['Close'].diff(1).fillna(0).rolling(window=rsi_period).apply(lambda x: -sum(x[x > 0]), raw=True))))
    data['SMA200'] = data['Close'].rolling(window=sma_period).mean()

    data['Buy_Signal'] = ((data['RSI'] < 30) & (data['RSI'].shift(1) < 30) & (data['RSI'].shift(2) < 30) &
                          (data['RSI'].shift(3) >= 30) & (data['RSI'].shift(4) >= 30) &
                          (data['RSI'].shift(5) < 60) & (data['RSI'].shift(4) < 60) &
                          (data['Close'] > data['SMA200']))

    data['Sell_Signal'] = (data['RSI'] > 50)

    return data


# User input for ticker symbol and starting date
ticker_symbol = input("Enter the ticker symbol: ")
start_date = input("Enter the starting date (YYYY-MM-DD): ")

# Use today's date as the end date
end_date = datetime.today().strftime('%Y-%m-%d')

# Retrieve historical stock price data from Yahoo Finance
data = yf.download(ticker_symbol, start=start_date, end=end_date)

# Define the parameter grid for RSI and SMA periods
param_grid = {
    'rsi_period': [3, 5, 7, 10, 14],
    'sma_period': [50, 100, 200, 300]
}

best_profit = float('-inf')
best_parameters = {}

# Iterate through the parameter grid
for params in ParameterGrid(param_grid):
    rsi_period = params['rsi_period']
    sma_period = params['sma_period']

    # Implement the trading strategy with current parameters
    data = implement_strategy(data.copy(), rsi_period, sma_period)

    # Calculate returns and simulate trading
    initial_balance = 10000  # Starting balance of $10,000
    balance = initial_balance
    shares_held = 0

    for i, row in data.iterrows():
        if row['Buy_Signal']:
            shares_to_buy = balance // row['Close']  # Buy as many shares as the account balance allows
            cost = shares_to_buy * row['Close']
            shares_held += shares_to_buy
            balance -= cost
        elif row['Sell_Signal']:
            balance += shares_held * row['Close']
            shares_held = 0

    profit = balance + shares_held * data['Close'].iloc[-1]

    if profit > best_profit:
        best_profit = profit
        best_parameters = params

# Implement the best strategy
best_rsi_period = best_parameters['rsi_period']
best_sma_period = best_parameters['sma_period']
data = implement_strategy(data, best_rsi_period, best_sma_period)

# Calculate daily returns
data['Returns'] = data['Balance'].pct_change()

# Create subplots
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

# Plot cumulative balance
ax1.plot(data.index, data['Balance'], label='Account Balance', color='blue')
ax1.set_ylabel('Account Balance', color='blue')
ax1.legend(loc='upper left')

# Plot buy and sell signals along with ticker price
ax2.plot(data.index, data['Close'], label='Ticker Price', color='orange', alpha=0.5)
ax2.scatter(data.index[data['Buy_Signal']], data['Close'][data['Buy_Signal']], marker='^', color='green', label='Buy Signal')
ax2.scatter(data.index[data['Sell_Signal']], data['Close'][data['Sell_Signal']], marker='v', color='red', label='Sell Signal')
ax2.set_ylabel('Ticker Price', color='orange')
ax2.legend(loc='upper right')

# Plot RSI
ax3.plot(data.index, data['RSI'], label='5-day RSI', color='purple')
ax3.axhline(y=30, color='red', linestyle='--', label='RSI 30')
ax3.axhline(y=60, color='green', linestyle='--', label='RSI 60')
ax3.fill_between(data.index, 30, 60, alpha=0.2, color='yellow')
ax3.set_xlabel('Date')
ax3.set_ylabel('RSI', color='purple')
ax3.legend(loc='upper left')

plt.title(f'Optimized Backtest Results for {ticker_symbol}')
plt.grid(True)

# Print the best parameters and profit
print(f'Optimal RSI Period: {best_rsi_period}')
print(f'Optimal SMA Period: {best_sma_period}')
print(f'Profit with Optimal Parameters: ${best_profit:.2f}')

# Save the plot to a JPG file
plt.savefig(f'{ticker_symbol}_optimized_backtest_results.jpg')

# Save the results to a CSV file
data.to_csv(f'{ticker_symbol}_optimized_backtest_results.csv')

# Show the plot
plt.show()
