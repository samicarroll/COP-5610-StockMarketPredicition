import os
import pandas as pd
import requests
import time

# Polygon.io API key 
POLYGON_API_KEY = 'piwQQBA2r0sXirdyCBdI5Wb9Sd_e7GOI'

START_DATE = "2021-08-01"
END_DATE = "2023-08-01"

# Define rate limiting parameters
REQUESTS_PER_MINUTE = 50  # Maximum number of requests allowed per minute
RATE_LIMIT_RESET_INTERVAL = 60  # Interval in seconds after which the request counter resets

# Initialize request counter and last reset time
request_counter = 0
last_reset_time = time.time()


def fetch_data_from_polygon(endpoint, ticker, start_date, end_date):
    """
    Fetches data from Polygon.io API for the specified endpoint and ticker.
    """
    global request_counter, last_reset_time

    try:
        # Check if rate limit needs to be enforced
        if request_counter >= REQUESTS_PER_MINUTE:
            # Calculate time remaining until the rate limit resets
            time_since_reset = time.time() - last_reset_time
            time_to_reset = max(0, RATE_LIMIT_RESET_INTERVAL - time_since_reset)
            print(f"Rate limit exceeded. Waiting {time_to_reset} seconds before next request.")
            time.sleep(time_to_reset)
            # Reset request counter and update last reset time
            request_counter = 0
            last_reset_time = time.time()

        # Fetch data from Polygon.io
        response = requests.get(f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}?apiKey={POLYGON_API_KEY}")
        if response.status_code == 200:
            # Increment request counter
            request_counter += 1

            data = response.json()
            if 'results' in data:
                return data['results']
            else:
                print(f"Failed to fetch data for {endpoint}. Unexpected response format.")
        else:
            print(f"Failed to fetch data for {endpoint}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to fetch data for {endpoint}: {e}")
    return None


def build_stock_dataset(start=START_DATE, end=END_DATE):
    """
    Creates the dataset containing all stock prices
    :returns: stock_prices.csv
    """
    global request_counter, last_reset_time

    statspath = "/Users/samcarroll/Documents/GitHub/COP-5610-StockMarketPredicition/intraQuarter"
    ticker_list = os.listdir(statspath)

    # Required on macOS
    if ".DS_Store" in ticker_list:
        os.remove(f"{statspath}/.DS_Store")
        ticker_list.remove(".DS_Store")

    # Initialize an empty DataFrame to store stock data
    df = pd.DataFrame()

    for ticker in ticker_list:
        ticker = ticker.upper()

        data = fetch_data_from_polygon("_KEYSTATS", ticker, start, end)
        if data:
            stock_data = pd.DataFrame(data)
            stock_data['t'] = pd.to_datetime(stock_data['t'], unit='ms')
            stock_data.set_index('t', inplace=True)
            stock_data = stock_data.rename(columns={"c": ticker})
            # Concatenate the stock data to the DataFrame
            df = pd.concat([df, stock_data[ticker]], axis=1)

    # Remove any rows with missing data
    df = df.dropna()

    # Save the DataFrame to a CSV file
    df.to_csv("stock_prices.csv")


def build_sp500_dataset(start=START_DATE, end=END_DATE):
    """
    Creates the dataset containing S&P500 prices
    :returns: sp500_index.csv
    """
    global request_counter, last_reset_time

    data = fetch_data_from_polygon("S&P500", "SPY", start, end)
    if data:
        sp500_data = pd.DataFrame(data)
        sp500_data['t'] = pd.to_datetime(sp500_data['t'], unit='ms')
        sp500_data.set_index('t', inplace=True)
        sp500_data = sp500_data.rename(columns={"c": "SPY"})
        # Save the data to a CSV file
        sp500_data.to_csv("sp500_index.csv")


if __name__ == "__main__":
    build_stock_dataset()
    build_sp500_dataset()
