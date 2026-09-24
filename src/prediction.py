import pandas as pd
import joblib


# Load data
data = pd.read_csv("outputs/model_data.csv")

# Load trained model
model = joblib.load("models/demand_model.pkl")


# Select product
product_id = input("Enter Product ID (example P1000): ")


# Get product data
product_data = data[
    data["product_id"] == product_id
].sort_values("month")


if len(product_data) == 0:

    print("\nProduct not found!")

else:

    # Get latest record
    latest = product_data.iloc[-1]

    # Create input using SAME 5 features
    input_data = pd.DataFrame([{
        "lag_1": latest["lag_1"],
        "lag_2": latest["lag_2"],
        "lag_3": latest["lag_3"],
        "rolling_mean_3": latest["rolling_mean_3"],
        "month_number": latest["month_number"]
    }])

    # Predict future demand
    predicted_demand = model.predict(
        input_data
    )[0]

    print("FUTURE DEMAND PREDICTION")

    print(
        "Product:",
        latest["product_name"]
    )

    print(
        "Category:",
        latest["category"]
    )

    print(
        "Predicted Demand:",
        round(predicted_demand, 0),
        "units"
    )