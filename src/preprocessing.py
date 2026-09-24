import pandas as pd


# Load both datasets
orders = pd.read_csv("data/orders.csv")
catalog = pd.read_csv("data/product_catalog.csv")


# Display basic information
print("Orders Dataset Shape:", orders.shape)
print("Product Catalog Shape:", catalog.shape)

print("\nOrders Columns:")
print(orders.columns.tolist())

print("\nCatalog Columns:")
print(catalog.columns.tolist())


# Convert order_date into proper date format
orders["order_date"] = pd.to_datetime(orders["order_date"])


# Basic dataset information
print("\nDate Range:")
print("Start Date:", orders["order_date"].min())
print("End Date:", orders["order_date"].max())

print("\nUnique Products:", orders["product_id"].nunique())
print("Unique Categories:", orders["category"].nunique())


# Check missing values
print("\nMissing Values in Orders:")
print(orders.isnull().sum())

print("\nMissing Values in Catalog:")
print(catalog.isnull().sum())


# Check duplicate rows
print("\nDuplicate Rows in Orders:", orders.duplicated().sum())
print("Duplicate Rows in Catalog:", catalog.duplicated().sum())