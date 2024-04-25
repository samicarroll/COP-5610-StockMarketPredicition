import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, roc_auc_score, precision_score, recall_score, f1_score

# Load data from keystats.csv
data = pd.read_csv("keystats.csv")

# Preprocess data
# For simplicity, let's drop rows with missing values and select numerical features
data.dropna(inplace=True)
features = data.select_dtypes(include='number').columns

X = data[features].values
y = data["Ticker"].values  # Assuming "Target" column contains the target labels

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train KNN classifier
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

knn_classifier = KNeighborsClassifier(n_neighbors=5)
knn_classifier.fit(X_train_scaled, y_train)

# Evaluate performance
y_pred = knn_classifier.predict(X_test_scaled)
print("KNN Classification Report:")
print(classification_report(y_test, y_pred))

# Obtain predicted probabilities for each class
y_pred_prob = knn_classifier.predict_proba(X_test_scaled)

# Extract probabilities for the positive class (assuming binary classification)
y_pred_prob_positive = y_pred_prob[:, 1]

# Calculate additional evaluation metrics
# Calculate precision, recall, and F1-score with 'macro' average setting
precision = precision_score(y_test, y_pred, average='macro', zero_division=0)
recall = recall_score(y_test, y_pred, average='macro', zero_division=0)
f1 = f1_score(y_test, y_pred, average='macro', zero_division=0)

# Calculate ROC AUC score
roc_auc = roc_auc_score(y_test, y_pred_prob_positive)

print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)
print("ROC-AUC:", roc_auc)
