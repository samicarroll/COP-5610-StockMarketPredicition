import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from utils import status_calc

# The percentage by which a stock has to beat the S&P500 to be considered a 'buy'
OUTPERFORMANCE = 15


def build_data_set():
    """
    Reads the keystats.csv file and prepares it for scikit-learn
    :return: X_train and y_train numpy arrays
    """
    training_data = pd.read_csv("keystats.csv", index_col="Date")
    training_data.dropna(axis=0, how="any", inplace=True)
    features = training_data.columns[6:]

    X_train = training_data[features].values
    # Generate the labels: '1' if a stock beats the S&P500 by more than 10%, else '0'.
    y_train = list(
        status_calc(
            training_data["stock_p_change"],
            training_data["SP500_p_change"],
            OUTPERFORMANCE,
        )
    )

    return X_train, y_train

def predict_stocks():
    X_train, y_train = build_data_set()
    
    # Split the data into train and test sets
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=0)
    
    # Create a pipeline for scaling and logistic regression
    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', LogisticRegression(max_iter=1000, random_state=0))
    ])
    
    # Define hyperparameters grid
    param_grid = {
        'classifier__C': [0.001, 0.01, 0.1, 1, 10, 100, 1000]
    }
    
    # Perform grid search for hyperparameter tuning
    grid_search = GridSearchCV(pipe, param_grid, cv=5, scoring='accuracy')
    grid_search.fit(X_train, y_train)
    
    # Get the best classifier from grid search
    best_clf = grid_search.best_estimator_
    
    # Evaluate the model on the validation set
    y_pred = best_clf.predict(X_val)
    print("Validation Report:")
    print(classification_report(y_val, y_pred))
    
    # Initialize an empty list to store predicted tickers
    invest_list = []
    
    # Iterate over each CSV file in the directory
    for file in os.listdir("forward/"):
        if file.endswith(".csv"):
            data = pd.read_csv(os.path.join("forward/", file), index_col="Date")
            data.dropna(axis=0, how="any", inplace=True)
            # Check if "Ticker" column exists in the DataFrame
            if "Ticker" in data.columns:
                features = data.columns[6:]
                X_test = data[features].values
                z = data["Ticker"].values

                # Get the predicted tickers
                y_pred = best_clf.predict(X_test)
                if sum(y_pred) != 0:
                    invest_list.extend(z[y_pred].tolist())

    if len(invest_list) == 0:
        print("No stocks predicted!")
    else:
        print(
            f"{len(invest_list)} stocks predicted to outperform the S&P500 by more than {OUTPERFORMANCE}%:"
        )
        print("\n".join(invest_list))
        return invest_list
    
if __name__ == "__main__":
    print("Building dataset and predicting stocks...")
    predict_stocks()