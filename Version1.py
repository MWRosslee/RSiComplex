import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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


# Retrieve historical stock price data from Yahoo Finance
ticker_symbol = 'AAPL'  # Replace with your desired ticker symbol
start_date = '2020-01-01'  # Replace with your desired start date
end_date = '2023-01-01'    # Replace with your desired end date
data = yf.download(ticker_symbol, start=start_date, end=end_date)

# Implement the trading strategy
data = implement_strategy(data)

# Calculate returns
data['Returns'] = np.where(data['Buy_Signal'], data['Close'].pct_change(), 0)
data['Cumulative_Returns'] = (1 + data['Returns']).cumprod()

# Plot cumulative returns
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Cumulative_Returns'], label='Cumulative Returns', color='blue')
plt.title(f'Backtest Results for {ticker_symbol}')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns')
plt.legend()
plt.grid(True)

# Plot buy and sell signals
plt.scatter(data.index[data['Buy_Signal']], data['Close'][data['Buy_Signal']], marker='^', color='green', label='Buy Signal')
plt.scatter(data.index[data['Sell_Signal']], data['Close'][data['Sell_Signal']], marker='v', color='red', label='Sell Signal')

plt.legend()

# Save the plot to a JPG file
plt.savefig(f'{ticker_symbol}_backtest_results.jpg')

# Save the results to a CSV file
data.to_csv(f'{ticker_symbol}_backtest_results.csv')

# Show the plot
plt.show()
