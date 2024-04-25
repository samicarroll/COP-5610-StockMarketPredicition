import pandas as pd
import os
import re
import time
import numpy as np
from tqdm import tqdm
import yfinance as yf  # Importing yfinance for Yahoo Finance API
from utils import data_string_to_float

# The path to your fundamental data
statspath = "intraQuarter/_KeyStats/"

# These are the features that will be parsed
features = [  # Valuation measures
    "Market Cap",
    "Enterprise Value",
    "Trailing P/E",
    "Forward P/E",
    "PEG Ratio",
    "Price/Sales",
    "Price/Book",
    "Enterprise Value/Revenue",
    "Enterprise Value/EBITDA",
    # Financials
    "Profit Margin",
    "Operating Margin",
    "Return on Assets",
    "Return on Equity",
    "Revenue",
    "Revenue Per Share",
    "Quarterly Revenue Growth",
    "Gross Profit",
    "EBITDA",
    "Net Income Avi to Common",
    "Diluted EPS",
    "Quarterly Earnings Growth",
    "Total Cash",
    "Total Cash Per Share",
    "Total Debt",
    "Total Debt/Equity",
    "Current Ratio",
    "Book Value Per Share",
    "Operating Cash Flow",
    "Levered Free Cash Flow",
    # Trading information
    "Beta",
    "50-Day Moving Average",
    "200-Day Moving Average",
    "Avg Vol (3 month)",
    "Shares Outstanding",
    "Float",
    "% Held by Insiders",
    "% Held by Institutions",
    "Shares Short",
    "Short Ratio",
    "Short % of Float",
    "Shares Short (prior month)",
]


def check_yahoo():
    """
    Retrieves the stock ticker from the _KeyStats directory, then downloads the html file from yahoo finance.
    :return: a directory named `forward/` filled with the html files for each ticker
    """
    # Create the directory where we will store the current data
    if not os.path.exists("forward/"):
        os.makedirs("forward/")

    # Retrieve a list of tickers from the fundamental data folder
    ticker_list = os.listdir(statspath)

    # Required in macOS to remove the hidden index file.
    if ".DS_Store" in ticker_list:
        ticker_list.remove(".DS_Store")

    for ticker in tqdm(ticker_list, desc="Download progress:", unit="tickers"):
        try:
            # Fetching stock data using Yahoo Finance API
            data = yf.Ticker(ticker)
            hist = data.history(period="1mo")  # Fetching 1 month historical data
            hist.to_html(f"forward/{ticker}.html")

        except Exception as e:
            print(f"{ticker}: {str(e)}\n")
            # If the symbol is delisted or not found, continue with the next ticker
            continue
        time.sleep(1)  # Add a delay to avoid hitting API rate limits


def forward():
    """
    Creates the forward sample by parsing the current data html files that we downloaded in check_yahoo().
    :return: a pandas dataframe containing all of the current data for each ticker.
    """
    # Creating an empty dataframe which we will later fill. In addition to the features, we need some index variables
    # (date, unix timestamp, ticker), and of course the dependent variables (prices).
    df_columns = [
        "Date",
        "Unix",
        "Ticker",
        "Price",
        "stock_p_change",
        "SP500",
        "SP500_p_change",
    ] + features

    df_list = []

    tickerfile_list = os.listdir("forward/")

    # Required in macOS to remove the hidden index file.
    if ".DS_Store" in tickerfile_list:
        tickerfile_list.remove(".DS_Store")

    # This is the actual parsing. This needs to be fixed every time yahoo changes their UI.
    for tickerfile in tqdm(tickerfile_list, desc="Parsing progress:", unit="tickers"):
        ticker = tickerfile.split(".html")[0].upper()

        try:
            # Fetching stock data using Yahoo Finance API
            data = yf.Ticker(ticker)
            hist = data.history(period="1mo")  # Fetching 1 month historical data
        except Exception as e:
            print(f"{ticker}: {str(e)}\n")
            # If the symbol is delisted or not found, continue with the next ticker
            continue

        # If no price data is found, skip this ticker
        if hist.empty:
            print(f"{ticker}: No price data found, symbol may be delisted\n")
            continue

        # Initialize values list to store feature values
        value_list = []

        # Iterate through each feature and fetch its value from the Yahoo Finance API
        for variable in features:
            try:
                value = hist[variable].iloc[0]  # Fetch value for the feature from historical data

                # Dealing with number formatting
                value_list.append(data_string_to_float(value))

            # The data may not be present. Process accordingly.
            except KeyError:
                value_list.append("N/A")
                # print(ticker, variable)

        # Append the ticker and the features to the dataframe
        new_df_row = [0, 0, ticker, 0, 0, 0, 0] + value_list

        df_list.append(new_df_row)

    df = pd.DataFrame(df_list, columns=df_columns)
    return df.replace("N/A", np.nan)

if __name__ == "__main__":
    check_yahoo()
    current_df = forward()
    current_df.to_csv("forward_sample.csv", index=False)