import os
import pandas as pd
import matplotlib.pyplot as plt

# Initialize an empty list to store data from CSV files
all_data = []

# Iterate over each CSV file in the forward/ directory
for file in os.listdir("forward/"):
    if file.endswith(".csv"):
        # Load data from the current CSV file
        data = pd.read_csv(os.path.join("forward/", file))
        # Add a new column with the file name as the label
        data['File'] = os.path.splitext(file)[0]
        all_data.append(data)

# Concatenate data from all CSV files into a single DataFrame
combined_data = pd.concat(all_data)

# Check if the combined DataFrame is not empty
if combined_data.empty:
    print("Error: No data found in the CSV files.")
    exit()

# Convert "Date" column to datetime format if needed
if "Date" in combined_data.columns:
    combined_data["Date"] = pd.to_datetime(combined_data["Date"])

# Plot the historical closing price of all stocks
plt.figure(figsize=(10, 6))
for file, stock_data in combined_data.groupby("File"):
    plt.plot(stock_data["Date"], stock_data["Close"], label=file)

plt.xlabel("Date")
plt.ylabel("Closing Price")
plt.title("Historical Closing Prices of Stocks (Grouped by File)")
plt.xticks(rotation=45)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(True)
plt.tight_layout()
plt.show()
