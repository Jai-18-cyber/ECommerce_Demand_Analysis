from src.preprocessing import orders
from src.demand_analysis import product_demand
from src.feature_engineering import model_data
from src.model import model

print("E-COMMERCE DEMAND ANALYSIS")


print("Total Orders:", orders["order_id"].nunique())
print("Total Products:", orders["product_id"].nunique())
print("Total Categories:", orders["category"].nunique())

print("\nProject Step 2 completed!")