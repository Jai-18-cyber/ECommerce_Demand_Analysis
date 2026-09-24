# E-Commerce Product Demand Analysis

A data-driven system for analyzing historical e-commerce sales data, identifying product demand trends, and estimating future product demand using Machine Learning.

## Problem Statement

E-commerce businesses generate large amounts of order data, but it can be difficult to identify:

* Best-selling and slow-moving products
* Changes in product demand over time
* Increasing and decreasing demand trends
* Expected future demand for products

This project analyzes historical order data and provides an interactive dashboard for demand analysis and future demand prediction.

## Objectives

* Analyze historical e-commerce order data
* Identify best-selling products
* Identify slow-moving products
* Analyze monthly demand patterns
* Detect increasing, decreasing, and stable demand
* Estimate future product demand using Machine Learning
* Provide an interactive dashboard for business insights

## Dataset

The project uses two datasets:

### 1. Orders Dataset

Contains historical transaction information.

* 61,193 order records
* 60 unique products
* 6 categories
* Data period: October 2023 – September 2025

Important columns:

* `order_id`
* `order_date`
* `product_id`
* `product_name`
* `category`
* `quantity`
* `unit_price`
* `revenue`

### 2. Product Catalog

Contains static information about the products.

* 60 products

Important columns:

* `product_id`
* `product_name`
* `category`
* `base_demand`
* `unit_price`

Both datasets are connected using `product_id`.

## Technologies Used

### Programming & Data Analysis

* Python
* Pandas
* NumPy

### Machine Learning

* Scikit-learn
* Random Forest Regressor
* Joblib

### Visualization & Dashboard

* Matplotlib
* Seaborn
* Streamlit

### Development

* Visual Studio Code
* Git & GitHub

## Project Workflow

```text
Historical Order Data
        ↓
Data Preprocessing
        ↓
Data Aggregation
        ↓
Product & Monthly Demand Analysis
        ↓
Demand Trend Detection
        ↓
Feature Engineering
        ↓
Random Forest Regression
        ↓
Future Demand Prediction
        ↓
Streamlit Dashboard
```

## Data Preprocessing

The preprocessing stage includes:

* Converting order dates into standard date format
* Checking missing values
* Checking duplicate records
* Validating product IDs
* Aggregating demand by product and month
* Calculating product-wise sales and revenue

## Demand Analysis

The system provides:

### Best-Selling Products

Products are ranked according to their total units sold.

### Slow-Moving Products

Products with comparatively lower sales volume are identified.

### Demand Trends

Demand is compared across the historical period and classified as:

* **Increasing** — demand increased significantly
* **Decreasing** — demand decreased significantly
* **Stable** — demand remained relatively stable

## Feature Engineering

For demand prediction, the following historical demand features are used:

* `lag_1` — previous month's demand
* `lag_2` — demand from two months earlier
* `lag_3` — demand from three months earlier
* `rolling_mean_3` — three-month rolling average demand

These features help the model learn recent demand patterns.

## Machine Learning Model

The project uses a **Random Forest Regressor** for future demand estimation.

The model is trained using historical demand features and predicts a numerical demand value in units.

### Model Configuration

```python
RandomForestRegressor(
    n_estimators=50,
    random_state=42
)
```

* `n_estimators=50` → 50 decision trees are used
* `random_state=42` → ensures reproducible results

### Evaluation

The model is evaluated using **Mean Absolute Error (MAE)**.

MAE represents the average absolute difference between actual and predicted demand.

## Dashboard

The Streamlit dashboard contains three main sections:

### 1. Overview

Provides:

* Year-wise business metrics
* Monthly insights
* Total orders
* Units sold
* Revenue
* Monthly demand chart
* Best-selling products
* Slow-moving products

### 2. Product Analysis

Allows users to:

* Select a category
* Select a product
* View latest demand
* View demand change
* Analyze the product's demand trend

### 3. Demand Prediction

Allows users to:

* Select a product
* View recent demand
* View recent demand trend
* Estimate future demand

## Project Structure

```text
ECommerce_Demand_Analysis/
│
├── data/
│   ├── orders.csv
│   └── product_catalog.csv
│
├── src/
│   ├── preprocessing.py
│   ├── demand_analysis.py
│   ├── feature_engineering.py
│   ├── model.py
│   └── prediction.py
│
├── models/
│   └── demand_model.pkl
│
├── outputs/
│   ├── product_demand.csv
│   ├── monthly_demand.csv
│   ├── trend_analysis.csv
│   ├── best_selling_products.csv
│   ├── slow_moving_products.csv
│   └── model_data.csv
│
├── app/
│   └── app.py
│
├── main.py
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/ECommerce_Demand_Analysis.git
```

Go to the project directory:

```bash
cd ECommerce_Demand_Analysis
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

## Run the Project

Run the Streamlit dashboard:

```bash
streamlit run app/app.py
```

The dashboard will open in your browser.

## Key Insights

The system helps businesses understand:

* Which products generate higher demand
* Which products are slow-moving
* How demand changes over time
* Which products show increasing or decreasing demand
* Estimated future demand based on recent historical patterns

## Future Scope

The project can be extended with:

* More advanced time-series forecasting models
* Seasonal demand analysis
* Holiday and festival effects
* Price-based demand analysis
* Inventory stock-out alerts
* Automated business recommendations
* Real-time sales data integration
* Cloud-based deployment

## Conclusion

The E-Commerce Product Demand Analysis system combines data analysis, demand trend detection, feature engineering, and Machine Learning to provide a practical approach for understanding product demand.

The interactive Streamlit dashboard makes the analysis easier to explore and supports data-driven decision-making for inventory and demand planning.

---

**Developed by:** Jai Porwal
**Domain:** Data Science
**Problem Statement:** PS-04
**Hackathon:** 2026
