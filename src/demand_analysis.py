import os
import pandas as pd
from src.preprocessing import orders

#CREATE OUTPUT FOLDER

os.makedirs("outputs", exist_ok=True)

#PRODUCT-WISE DEMAND ANALYSIS

product_demand = (
    orders.groupby(
        ["product_id", "product_name", "category"]
    )
    .agg(
        total_quantity=("quantity", "sum"),
        total_revenue=("revenue", "sum"),
        number_of_orders=("order_id", "nunique")
    )
    .reset_index()
)

#BEST-SELLING PRODUCTS
best_selling = (
    product_demand
    .sort_values(
        "total_quantity",
        ascending=False
    )
    .head(10)
)
print("TOP 10 BEST-SELLING PRODUCTS")

print(
    best_selling.to_string(index=False)
)

#SLOW-MOVING PRODUCTS

slow_moving = (
    product_demand
    .sort_values(
        "total_quantity",
        ascending=True
    )
    .head(10)
)
print("TOP 10 SLOW-MOVING PRODUCTS")

print(
    slow_moving.to_string(index=False)
)

# 5. CREATE MONTH COLUMN
orders["month"] = (
    orders["order_date"]
    .dt.to_period("M")
    .dt.to_timestamp()
)

#MONTHLY PRODUCT DEMAND
monthly_demand = (
    orders.groupby(
        [
            "month",
            "product_id",
            "product_name",
            "category"
        ]
    )
    .agg(
        demand=("quantity", "sum"),
        revenue=("revenue", "sum"),
        number_of_orders=("order_id", "nunique")
    )
    .reset_index()
)


#DEMAND TREND ANALYSIS


# Calculate first and last month demand
first_month = (
    monthly_demand
    .sort_values("month")
    .groupby("product_id")
    .first()
    .reset_index()
)

last_month = (
    monthly_demand
    .sort_values("month")
    .groupby("product_id")
    .last()
    .reset_index()
)


# Keep only required columns
first_month = first_month[
    ["product_id", "demand"]
].rename(
    columns={"demand": "first_month_demand"}
)

last_month = last_month[
    ["product_id", "demand"]
].rename(
    columns={"demand": "last_month_demand"}
)


# Merge first and last month demand
trend_analysis = product_demand.merge(
    first_month,
    on="product_id",
    how="left"
)

trend_analysis = trend_analysis.merge(
    last_month,
    on="product_id",
    how="left"
)

#DEMAND CHANGE %

trend_analysis["demand_change_percent"] = (
    (
        trend_analysis["last_month_demand"]
        - trend_analysis["first_month_demand"]
    )
    /
    trend_analysis["first_month_demand"].replace(0, 1)
) * 100

#CLASSIFY DEMAND TREND
def classify_trend(change):

    if change > 10:
        return "Increasing"

    elif change < -10:
        return "Decreasing"

    else:
        return "Stable"


trend_analysis["trend"] = (
    trend_analysis["demand_change_percent"]
    .apply(classify_trend)
)

#DISPLAY TREND RESULTS
print("DEMAND TREND ANALYSIS")

print(
    trend_analysis[
        [
            "product_id",
            "product_name",
            "category",
            "first_month_demand",
            "last_month_demand",
            "demand_change_percent",
            "trend"
        ]
    ]
    .sort_values(
        "demand_change_percent",
        ascending=False
    )
    .head(15)
    .to_string(index=False)
)

#SAVE PRODUCT DEMAND DATA

product_demand.to_csv(
    "outputs/product_demand.csv",
    index=False
)


#SAVE MONTHLY DEMAND DATA

monthly_demand.to_csv(
    "outputs/monthly_demand.csv",
    index=False
)

#SAVE TREND ANALYSIS

trend_analysis.to_csv(
    "outputs/trend_analysis.csv",
    index=False
)

#SAVE BEST-SELLING PRODUCTS

best_selling.to_csv(
    "outputs/best_selling_products.csv",
    index=False
)
#SAVE SLOW-MOVING PRODUCTS
slow_moving.to_csv(
    "outputs/slow_moving_products.csv",
    index=False
)

#FINAL MESSAGE

print("DEMAND ANALYSIS COMPLETED")

print("Created files:")

print("1. outputs/product_demand.csv")
print("2. outputs/monthly_demand.csv")
print("3. outputs/trend_analysis.csv")
print("4. outputs/best_selling_products.csv")
print("5. outputs/slow_moving_products.csv")

print("\nStep 2 completed successfully!")