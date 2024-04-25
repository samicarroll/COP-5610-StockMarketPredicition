import pandas as pd
import os
import re
import time
import yfinance as yf
import numpy as np
from tqdm import tqdm
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
    "Shares Short (prior month",
]

def check_yahoo():
    """
    Retrieves the stock ticker from the _KeyStats directory, then downloads the data from Yahoo Finance using the yfinance library.
    :return: a directory named `forward/` filled with the data files for each ticker
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
            hist = data.history(period="10y")  # Fetching 1o years of historical data
            hist.to_csv(f"forward/{ticker}.csv")

        except Exception as e:
            print(f"{ticker}: {str(e)}\n")
            time.sleep(2)


if __name__ == "__main__":
    check_yahoo()
