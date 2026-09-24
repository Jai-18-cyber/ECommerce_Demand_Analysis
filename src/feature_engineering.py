import os
import pandas as pd


#CREATE OUTPUT FOLDER
os.makedirs("outputs", exist_ok=True)
# 2. LOAD MONTHLY DEMAND DATA
monthly_demand = pd.read_csv(
    "outputs/monthly_demand.csv"
)
# Convert month column into datetime
monthly_demand["month"] = pd.to_datetime(
    monthly_demand["month"]
)

# Sort data properly
monthly_demand = monthly_demand.sort_values(
    ["product_id", "month"]
)
#CREATE LAG FEATURES
# Previous month's demand
monthly_demand["lag_1"] = (
    monthly_demand
    .groupby("product_id")["demand"]
    .shift(1)
)

# Demand two months ago
monthly_demand["lag_2"] = (
    monthly_demand
    .groupby("product_id")["demand"]
    .shift(2)
)

# Demand three months ago
monthly_demand["lag_3"] = (
    monthly_demand
    .groupby("product_id")["demand"]
    .shift(3)
)
#CREATE ROLLING AVERAGE
monthly_demand["rolling_mean_3"] = (
    monthly_demand
    .groupby("product_id")["demand"]
    .transform(
        lambda x: x.shift(1).rolling(3).mean()
    )
)
#CREATE MONTH FEATURE
monthly_demand["month_number"] = (
    monthly_demand["month"].dt.month
)
#REMOVE ROWS WITH MISSING FEATURES
model_data = monthly_demand.dropna(
    subset=[
        "lag_1",
        "lag_2",
        "lag_3",
        "rolling_mean_3"
    ]
).copy()
#SELECT MODEL FEATURES
features = [
    "lag_1",
    "lag_2",
    "lag_3",
    "rolling_mean_3",
    "month_number"
]
target = "demand"
#DISPLAY INFORMATION
print("FEATURE ENGINEERING")
print("Original Rows:", len(monthly_demand))
print("Rows After Feature Creation:", len(model_data))
print("\nFeatures Used:")
for feature in features:
    print("-", feature)
print("\nTarget Variable:")
print("-", target)
#DISPLAY SAMPLE DATA
print("SAMPLE MODEL DATA")
print(
    model_data[
        [
            "product_id",
            "month",
            "demand",
            "lag_1",
            "lag_2",
            "lag_3",
            "rolling_mean_3",
            "month_number"
        ]
    ]
    .head(10)
    .to_string(index=False)
)
#SAVE FEATURE DATA
model_data.to_csv(
    "outputs/model_data.csv",
    index=False
)
#FINAL MESSAGE
print("FEATURE ENGINEERING COMPLETED")
print(
    "Created file: outputs/model_data.csv"
)