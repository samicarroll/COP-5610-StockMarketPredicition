#!/bin/bash

echo "------------ installing requirements ------------"
pip install -r requirements.txt

echo "------------ running 'download_historical_prices' ------------"
python3 download_historical_prices.py

echo "------------ running 'parsing_keystats' ------------"
python3 parsing_keystats.py

echo "------------ running 'backtesting' ------------"
python3 backtesting.py

# echo "------------ running 'current_data' ------------"
# python3 current_data.py

echo "------------ running 'pytest' ------------"
pytest -v

echo "------------ running 'stock prediction' ------------"
python3 stock_prediction.py

# EOF