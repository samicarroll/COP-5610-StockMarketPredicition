import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score
from utils import status_calc

def backtest():
    """
    A simple backtest, which splits the dataset into a train set and test set,
    then fits a Random Forest classifier to the train set. We print the precision and accuracy
    of the classifier on the test set, then run a backtest comparing this strategy's performance
    to passive investment in the S&P500.
    Please note that there is a methodological flaw in this backtest which will give deceptively
    good results, so the results here should not encourage you to live trade.
    """
    # Load the dataset and drop any rows with missing values
    data_df = pd.read_csv("keystats.csv", index_col="Date")
    data_df.dropna(axis=0, how="any", inplace=True)

    features = data_df.columns[6:]
    X = data_df[features].values
    y = list(status_calc(data_df["stock_p_change"], data_df["SP500_p_change"], outperformance=10))
    z = np.array(data_df[["stock_p_change", "SP500_p_change"]])

    # Calculate the minimum number of samples required for the test set
    min_test_samples = int(len(X) * 0.2)

    if min_test_samples == 0:
        raise ValueError("Test size is too large relative to the dataset size")

    # Ensure that there are enough samples for both the training and test sets
    X_train, X_test, y_train, y_test, z_train, z_test = train_test_split(
        X, y, z, test_size=min(0.2, min_test_samples / len(X))
    )

    # Instantiate a RandomForestClassifier with 100 trees, then fit it to the training data
    clf = RandomForestClassifier(n_estimators=100, random_state=0)
    clf.fit(X_train, y_train)

    # Generate the predictions, then print test set accuracy and precision
    y_pred = clf.predict(X_test)
    print("Classifier performance\n", "=" * 20)
    print(f"Accuracy score: {clf.score(X_test, y_test): .2f}")
    print(f"Precision score: {precision_score(y_test, y_pred): .2f}")

    # Calculate the number of positive predictions
    num_positive_predictions = sum(y_pred)
    if num_positive_predictions < 0:
        print("No stocks predicted!")

    # Calculate stock and market returns
    stock_returns = 1 + z_test[y_pred, 0] / 100
    market_returns = 1 + z_test[y_pred, 1] / 100

    # Calculate average growth for each stock and the corresponding index growth
    avg_predicted_stock_growth = sum(stock_returns) / num_positive_predictions
    index_growth = sum(market_returns) / num_positive_predictions
    percentage_stock_returns = 100 * (avg_predicted_stock_growth - 1)
    percentage_market_returns = 100 * (index_growth - 1)
    total_outperformance = percentage_stock_returns - percentage_market_returns

    print("\n Stock prediction performance report \n", "=" * 40)
    print(f"Total Trades:", num_positive_predictions)
    print(f"Average return for stock predictions: {percentage_stock_returns: .1f} %")
    print(f"Average market return in the same period: {percentage_market_returns: .1f}% ")
    print(f"Compared to the index, our strategy earns {total_outperformance: .1f} percentage points more")

if __name__ == "__main__":
    backtest()
