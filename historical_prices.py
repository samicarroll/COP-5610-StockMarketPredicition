import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the forward_sample.csv file
data = pd.read_csv("forward_sample.csv")

# Select a specific stock ticker for visualization
ticker = "AAPL"  # Example: Apple Inc. ticker

# Filter the data for the selected stock ticker
stock_data = data.loc[data["Ticker"] == ticker].copy()

# Check if the stock_data DataFrame is not empty
if stock_data.empty:
    print(f"No data found for {ticker}")
else:
    # Convert "Date" column to datetime format if needed
    stock_data["Date"] = pd.to_datetime(stock_data["Date"])

    # Plot the historical closing price of the selected stock
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data["Date"], stock_data["Price"], label="Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(f"Historical Closing Price of {ticker}")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
