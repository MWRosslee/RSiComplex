import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Define a function to calculate the Relative Strength Index (RSI)
def calculate_rsi(data, period):
    delta = data.diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

# Define your trading strategy rules for Aggressive
def aggressive_strategy(data):
    # Calculate the 5-day RSI and 200-day SMA
    data['RSI_5'] = calculate_rsi(data['Close'], 5)
    data['SMA_200'] = data['Close'].rolling(window=200).mean()

    # Calculate the 'Balance' column based on the trading strategy
    data['Balance'] = 10000  # Starting balance
    shares_held = 0

    # Lists to log trades and buy/sell triggers
    trades = []
    buy_triggers = []
    sell_triggers = []

    for i, row in data.iterrows():
        # Define suggested buy and sell conditions for Aggressive strategy
        buy_condition = (
            (row['RSI_5'] < 30) and
            (row['RSI_5'] < data['RSI_5'].shift(1)) and
            (row['RSI_5'] < data['RSI_5'].shift(2)) and
            (row['Close'] > row['SMA_200'])
        )

        sell_condition = (
            (row['RSI_5'] > 50)
        )

        if buy_condition:
            shares_to_buy = data['Balance'][i] // row['Close']  # Buy as many shares as the account balance allows
            cost = shares_to_buy * row['Close']
            shares_held += shares_to_buy
            data.at[i, 'Balance'] -= cost

            # Log the trade and buy trigger
            trades.append(f"Buy: {shares_to_buy} shares at {row['Close']:.2f}")
            buy_triggers.append(f"{i}: Buy Trigger")

        elif sell_condition:
            data.at[i, 'Balance'] += shares_held * row['Close']
            shares_held = 0

            # Log the trade and sell trigger
            trades.append(f"Sell: {shares_held} shares at {row['Close']:.2f}")
            sell_triggers.append(f"{i}: Sell Trigger")

    # Create a DataFrame to store trade logs
    trade_log = pd.DataFrame({'Trades': trades, 'Buy Triggers': buy_triggers, 'Sell Triggers': sell_triggers})

    # Save trade log to a CSV file
    trade_log.to_csv('trade_log_aggressive.csv', index=False)

    return data

# Define your trading strategy rules for Moderate
def moderate_strategy(data):
    # Calculate the 5-day RSI and 200-day SMA
    data['RSI_5'] = calculate_rsi(data['Close'], 5)
    data['SMA_200'] = data['Close'].rolling(window=200).mean()

    # Calculate the 'Balance' column based on the trading strategy
    data['Balance'] = 10000  # Starting balance
    shares_held = 0

    # Lists to log trades and buy/sell triggers
    trades = []
    buy_triggers = []
    sell_triggers = []

    for i, row in data.iterrows():
        # Define suggested buy and sell conditions for Moderate strategy
        buy_condition = (
            (row['RSI_5'] < 30) and
            (data['RSI_5'].shift(1) < 30).all() and
            (data['RSI_5'].shift(2) < 30).all() and
            (row['Close'] > data['SMA_200'])
        )

        sell_condition = (
            (row['RSI_5'] > 50)
        )

        if buy_condition:
            shares_to_buy = data['Balance'][i] // row['Close']  # Buy as many shares as the account balance allows
            cost = shares_to_buy * row['Close']
            shares_held += shares_to_buy
            data.at[i, 'Balance'] -= cost

            # Log the trade and buy trigger
            trades.append(f"Buy: {shares_to_buy} shares at {row['Close']:.2f}")
            buy_triggers.append(f"{i}: Buy Trigger")

        elif sell_condition:
            data.at[i, 'Balance'] += shares_held * row['Close']
            shares_held = 0

            # Log the trade and sell trigger
            trades.append(f"Sell: {shares_held} shares at {row['Close']:.2f}")
            sell_triggers.append(f"{i}: Sell Trigger")

    # Create a DataFrame to store trade logs
    trade_log = pd.DataFrame({'Trades': trades, 'Buy Triggers': buy_triggers, 'Sell Triggers': sell_triggers})

    # Save trade log to a CSV file
    trade_log.to_csv('trade_log_moderate.csv', index=False)

    return data

# Define your trading strategy rules for Conservative

    print("Length of trades:", len(trades))
    print("Length of buy_triggers:", len(buy_triggers))
    print("Length of sell_triggers:", len(sell_triggers))
def aggressive_strategy(data):
    # Calculate the 5-day RSI and 200-day SMA
    data['RSI_5'] = calculate_rsi(data['Close'], 5)
    data['SMA_200'] = data['Close'].rolling(window=200).mean()

    # Calculate the 'Balance' column based on the trading strategy
    data['Balance'] = 10000  # Starting balance
    shares_held = 0

    # Lists to log trades and buy/sell triggers
    trades = []
    buy_triggers = []
    sell_triggers = []

    for i, row in data.iterrows():
        # Define suggested buy and sell conditions for Aggressive strategy
        buy_condition = (
            (row['RSI_5'] < 30) and
            (row['RSI_5'] < data['RSI_5'].shift(1)) and
            (row['RSI_5'] < data['RSI_5'].shift(2)) and
            (row['Close'] > row['SMA_200'])
        )

        sell_condition = (
            (row['RSI_5'] > 50)
        )

        if buy_condition:
            shares_to_buy = data['Balance'][i] // row['Close']  # Buy as many shares as the account balance allows
            cost = shares_to_buy * row['Close']
            shares_held += shares_to_buy
            data.at[i, 'Balance'] -= cost

            # Log the trade and buy trigger
            trades.append(f"Buy: {shares_to_buy} shares at {row['Close']:.2f}")
            buy_triggers.append(f"{i}: Buy Trigger")

        elif sell_condition:
            data.at[i, 'Balance'] += shares_held * row['Close']
            shares_held = 0

            # Log the trade and sell trigger
            trades.append(f"Sell: {shares_held} shares at {row['Close']:.2f}")
            sell_triggers.append(f"{i}: Sell Trigger")

    # Create a DataFrame to store trade logs
    trade_log = pd.DataFrame({'Trades': trades, 'Buy Triggers': buy_triggers, 'Sell Triggers': sell_triggers})

    # Save trade log to a CSV file
    trade_log.to_csv('trade_log_aggressive.csv', index=False)

    return data

# Define your trading strategy rules for Moderate
def moderate_strategy(data):
    # Calculate the 5-day RSI and 200-day SMA
    data['RSI_5'] = calculate_rsi(data['Close'], 5)
    data['SMA_200'] = data['Close'].rolling(window=200).mean()

    # Calculate the 'Balance' column based on the trading strategy
    data['Balance'] = 10000  # Starting balance
    shares_held = 0

    # Lists to log trades and buy/sell triggers
    trades = []
    buy_triggers = []
    sell_triggers = []

    for i, row in data.iterrows():
        # Define suggested buy and sell conditions for Moderate strategy
        buy_condition = (
            (row['RSI_5'] < 30) and
            (data['RSI_5'].shift(1) < 30).all() and
            (data['RSI_5'].shift(2) < 30).all() and
            (row['Close'] > data['SMA_200'])
        )

        sell_condition = (
            (row['RSI_5'] > 50)
        )

        if buy_condition:
            shares_to_buy = data['Balance'][i] // row['Close']  # Buy as many shares as the account balance allows
            cost = shares_to_buy * row['Close']
            shares_held += shares_to_buy
            data.at[i, 'Balance'] -= cost

            # Log the trade and buy trigger
            trades.append(f"Buy: {shares_to_buy} shares at {row['Close']:.2f}")
            buy_triggers.append(f"{i}: Buy Trigger")

        elif sell_condition:
            data.at[i, 'Balance'] += shares_held * row['Close']
            shares_held = 0

            # Log the trade and sell trigger
            trades.append(f"Sell: {shares_held} shares at {row['Close']:.2f}")
            sell_triggers.append(f"{i}: Sell Trigger")

    # Create a DataFrame to store trade logs
    trade_log = pd.DataFrame({'Trades': trades, 'Buy Triggers': buy_triggers, 'Sell Triggers': sell_triggers})

    # Save trade log to a CSV file
    trade_log.to_csv('trade_log_moderate.csv', index=False)

    return data

# Define your trading strategy rules for Conservative
def conservative_strategy(data):
    # Calculate the 5-day RSI and 200-day SMA
    data['RSI_5'] = calculate_rsi(data['Close'], 5)
    data['SMA_200'] = data['Close'].rolling(window=200).mean()

    # Calculate the 'Balance' column based on the trading strategy
    data['Balance'] = 10000  # Starting balance
    shares_held = 0

    # Lists to log trades and buy/sell triggers
    trades = []
    buy_triggers = []
    sell_triggers = []

    for i, row in data.iterrows():
        # Define suggested buy and sell conditions for Conservative strategy
        buy_condition = (
            (row['RSI_5'] < 30) and
            (data['RSI_5'].shift(1) < 30).all() and
            (data['RSI_5'].shift(2) < 30).all() and
            (row['Close'] > data['SMA_200'])
        )

        sell_condition = (
            (row['RSI_5'] > 50)
        )

        if buy_condition:
            shares_to_buy = data['Balance'][i] // row['Close']  # Buy as many shares as the account balance allows
            cost = shares_to_buy * row['Close']
            shares_held += shares_to_buy
            data.at[i, 'Balance'] -= cost

            # Log the trade and buy trigger
            trades.append(f"Buy: {shares_to_buy} shares at {row['Close']:.2f}")
            buy_triggers.append(f"{i}: Buy Trigger")

        elif sell_condition:
            data.at[i, 'Balance'] += shares_held * row['Close']
            shares_held = 0

            # Log the trade and sell trigger
            trades.append(f"Sell: {shares_held} shares at {row['Close']:.2f}")
            sell_triggers.append(f"{i}: Sell Trigger")

    # Create a DataFrame to store trade logs
    trade_log = pd.DataFrame({'Trades': trades, 'Buy Triggers': buy_triggers, 'Sell Triggers': sell_triggers})

    # Save trade log to a CSV file
    trade_log.to_csv('trade_log_conservative.csv', index=False)

    return data

# User input for ticker symbol, starting date, and strategy selection
ticker_symbol = input("Enter the ticker symbol: ")
start_date = input("Enter the starting date (YYYY-MM-DD): ")
strategy_selection = input("Select strategy (A for Aggressive, M for Moderate, C for Conservative, or a combination separated by commas): ")

# Use today's date as the end date
end_date = datetime.today().strftime('%Y-%m-%d')

# Create a dictionary to map first letters to strategy names
strategy_mapping = {
    'A': 'Aggressive',
    'M': 'Moderate',
    'C': 'Conservative'
}

# Split the user's strategy selection
selected_strategies = strategy_selection.split(',')

# Initialize variables to store combined results
combined_data = pd.DataFrame()
combined_profit = 0

# Create subplots and generate plots as needed
fig, axs = plt.subplots(len(selected_strategies) + 1, figsize=(10, 8), sharex=True)

# Iterate through selected strategies
for idx, selected_strategy in enumerate(selected_strategies):
    selected_strategy = selected_strategy.strip().upper()  # Remove leading/trailing spaces and convert to uppercase
    full_strategy_name = strategy_mapping.get(selected_strategy)

    if full_strategy_name:
        # Retrieve historical stock price data from Yahoo Finance
        data = yf.download(ticker_symbol, start=start_date, end=end_date)

        # Implement the trading strategy for the selected strategy
        if full_strategy_name == 'Aggressive':
            data = aggressive_strategy(data)
        elif full_strategy_name == 'Moderate':
            data = moderate_strategy(data)
        elif full_strategy_name == 'Conservative':
            data = conservative_strategy(data)

        # Calculate daily returns
        data['Returns'] = data['Balance'].pct_change()

        # Store individual strategy results
        combined_data[full_strategy_name] = data['Balance']

        # Update combined profit
        combined_profit += data['Balance'][-1]

        # Plot the balance for the selected strategy
        axs[idx].plot(data.index, data['Balance'], label=f'{full_strategy_name} Balance')
        axs[idx].set_ylabel('Balance')

# Plot the combined balance
axs[-1].plot(combined_data.index, combined_data.sum(axis=1), label='Combined Balance', color='black')
axs[-1].set_ylabel('Combined Balance')

# Set x-axis label for the last subplot
axs[-1].set_xlabel('Date')

# Add legend to all subplots
for ax in axs:
    ax.legend()

# Print the combined profit
print(f'Combined Profit with Selected Strategies: ${combined_profit:.2f}')

# Show the plot
plt.show()
