import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


# Define your trading strategy rules
def implement_strategy(data):
    data['RSI'] = 100 - (100 / (1 + (data['Close'].diff(1).fillna(0).rolling(window=5).apply(lambda x: sum(x[x < 0]), raw=True) /
                                 data['Close'].diff(1).fillna(0).rolling(window=5).apply(lambda x: -sum(x[x > 0]), raw=True))))
    data['SMA200'] = data['Close'].rolling(window=200).mean()

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

# Implement the trading strategy
data = implement_strategy(data)

# Calculate returns
data['Returns'] = np.where(data['Buy_Signal'], data['Close'].pct_change(), 0)
data['Cumulative_Returns'] = (1 + data['Returns']).cumprod()

# Plot cumulative returns
fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.plot(data.index, data['Cumulative_Returns'], label='Cumulative Returns', color='blue')
ax1.set_xlabel('Date')
ax1.set_ylabel('Cumulative Returns', color='blue')
ax1.legend(loc='upper left')

# Plot buy and sell signals
ax2 = ax1.twinx()
ax2.plot(data.index, data['Close'], label='Ticker Price', color='orange', alpha=0.5)
ax2.scatter(data.index[data['Buy_Signal']], data['Close'][data['Buy_Signal']], marker='^', color='green', label='Buy Signal')
ax2.scatter(data.index[data['Sell_Signal']], data['Close'][data['Sell_Signal']], marker='v', color='red', label='Sell Signal')
ax2.set_ylabel('Ticker Price', color='orange')
ax2.legend(loc='upper right')

plt.title(f'Backtest Results for {ticker_symbol}')
plt.grid(True)

# Save the plot to a JPG file
plt.savefig(f'{ticker_symbol}_backtest_results.jpg')

# Save the results to a CSV file
data.to_csv(f'{ticker_symbol}_backtest_results.csv')

# Show the plot
plt.show()
