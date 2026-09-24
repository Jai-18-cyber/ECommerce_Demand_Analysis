import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

#CREATE REQUIRED FOLDERS
os.makedirs("models", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
# LOAD MODEL DATA
data = pd.read_csv(
    "outputs/model_data.csv"
)
#SORT DATA BY TIME
data["month"] = pd.to_datetime(
    data["month"]
)
data = data.sort_values(
    ["month", "product_id"]
).reset_index(drop=True)
#SELECT FEATURES AND TARGET
features = [
    "lag_1",
    "lag_2",
    "lag_3",
    "rolling_mean_3",
    "month_number"
]
target = "demand"
X = data[features]
y = data[target]
#TIME-BASED TRAIN TEST SPLIT
split_index = int(len(data) * 0.8)
X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]
y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]
print("ML MODEL TRAINING")
print("Training Samples:", len(X_train))
print("Testing Samples:", len(X_test))
#CREATE RANDOM FOREST MODEL
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    random_state=42
)
#TRAIN MODEL
model.fit(
    X_train,
    y_train
)
print("\nModel training completed!")
#MAKE TEST PREDICTIONS
predictions = model.predict(
    X_test
)
#CALCULATE MAE
mae = mean_absolute_error(
    y_test,
    predictions
)
#CALCULATE RMSE
rmse = mean_squared_error(
    y_test,
    predictions
) ** 0.5
#DISPLAY MODEL PERFORMANCE
print("MODEL PERFORMANCE")
print("MAE :", round(mae, 2))
print("RMSE:", round(rmse, 2))
#SAVE MODEL
joblib.dump(
    model,
    "models/demand_model.pkl"
)
#SAVE MODEL METRICS
metrics = pd.DataFrame({
    "Metric": [
        "Mean Absolute Error",
        "Root Mean Squared Error"
    ],
    "Value": [
        mae,
        rmse
    ]
})


metrics.to_csv(
    "outputs/model_metrics.csv",
    index=False
)


#SAVE TEST PREDICTIONS

test_results = data.iloc[
    split_index:
].copy()

test_results["predicted_demand"] = predictions

test_results.to_csv(
    "outputs/test_predictions.csv",
    index=False
)


#FINAL MESSAGE

print("MODEL SAVED SUCCESSFULLY")


print(
    "Model: models/demand_model.pkl"
)

print(
    "Metrics: outputs/model_metrics.csv"
)

print(
    "Predictions: outputs/test_predictions.csv"
)

print("\nStep 4 completed successfully!")