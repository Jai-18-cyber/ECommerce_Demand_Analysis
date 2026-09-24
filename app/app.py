import streamlit as st
import pandas as pd
import joblib

# PAGE CONFIGURATION


st.set_page_config(
    page_title="E-Commerce Demand Analysis",
    layout="wide"
)

# LOAD DATA


orders = pd.read_csv("data/orders.csv")
model_data = pd.read_csv("outputs/model_data.csv")

model_data["month"] = pd.to_datetime(model_data["month"])
orders["order_date"] = pd.to_datetime(orders["order_date"])

model = joblib.load("models/demand_model.pkl")

# PRODUCT LIST


products = (
    orders[
        ["product_id", "product_name", "category"]
    ]
    .drop_duplicates()
    .sort_values("product_name")
)

# SIDEBAR


with st.sidebar:

    st.title("Demand Analysis")

    st.caption(
        "E-Commerce Product Demand Analysis"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Product Analysis",
            "Demand Prediction"
        ]
    )

    st.divider()

    st.caption("Data Period")

    st.write(
        orders["order_date"].min().strftime("%d %b %Y")
        + " - "
        + orders["order_date"].max().strftime("%d %b %Y")
    )

# MAIN TITLE


st.title("E-Commerce Demand Analysis")

st.write(
    "Analyze product sales, demand trends and future demand."
)

# PAGE 1: OVERVIEW


if page == "Overview":

    st.header("Business Overview")

    
    # YEAR SELECTION
    

    available_years = sorted(
        orders["order_date"].dt.year.unique()
    )

    selected_year = st.selectbox(
        "Select Year",
        available_years,
        index=len(available_years) - 1
    )

    year_data = orders[
        orders["order_date"].dt.year == selected_year
    ]

    # YEARLY METRICS
    

    total_products = year_data["product_id"].nunique()

    total_orders = year_data["order_id"].nunique()

    total_units = year_data["quantity"].sum()

    total_revenue = year_data["revenue"].sum()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Products",
            f"{total_products:,}"
        )

    with col2:
        st.metric(
            "Orders",
            f"{total_orders:,}"
        )

    with col3:
        st.metric(
            "Units Sold",
            f"{total_units:,}"
        )

    with col4:
        st.metric(
            "Revenue",
            f"₹{total_revenue:,.0f}"
        )

    
    # MONTH SELECTION
    

    month_names = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }

    available_months = sorted(
        year_data["order_date"].dt.month.unique()
    )

    selected_month = st.selectbox(
        "Select Month",
        available_months,
        format_func=lambda x: month_names[x]
    )

    month_data = year_data[
        year_data["order_date"].dt.month == selected_month
    ]

    
    # MONTHLY INSIGHTS
    

    st.subheader(
        f"Monthly Insights - "
        f"{month_names[selected_month]} {selected_year}"
    )

    monthly_products = month_data[
        "product_id"
    ].nunique()

    monthly_orders = month_data[
        "order_id"
    ].nunique()

    monthly_units = month_data[
        "quantity"
    ].sum()

    monthly_revenue = month_data[
        "revenue"
    ].sum()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Products",
            f"{monthly_products:,}"
        )

    with col2:
        st.metric(
            "Orders",
            f"{monthly_orders:,}"
        )

    with col3:
        st.metric(
            "Units Sold",
            f"{monthly_units:,}"
        )

    with col4:
        st.metric(
            "Revenue",
            f"₹{monthly_revenue:,.0f}"
        )

    
    # MONTHLY DEMAND CHART
    

    st.subheader(
        f"Monthly Demand - {selected_year}"
    )

    monthly_demand = (
        year_data
        .groupby(
            year_data["order_date"].dt.month
        )["quantity"]
        .sum()
        .reset_index()
    )

    monthly_demand.columns = [
        "Month",
        "Units Sold"
    ]

    monthly_demand["Month"] = (
        monthly_demand["Month"]
        .map(month_names)
    )

    st.bar_chart(
        monthly_demand.set_index("Month"),
        height=350
    )

    
    # MONTHLY DATA TABLE
    

    with st.expander(
        "View Monthly Demand Data"
    ):

        st.dataframe(
            monthly_demand,
            use_container_width=True,
            hide_index=True
        )

    
    # SELECTED MONTH PRODUCT PERFORMANCE
    
    st.subheader(
        f"Product Performance - "
        f"{month_names[selected_month]} {selected_year}"
    )

    product_summary = (
        month_data
        .groupby(
            [
                "product_id",
                "product_name",
                "category"
            ]
        )
        .agg(
            Units_Sold=("quantity", "sum"),
            Revenue=("revenue", "sum"),
            Orders=("order_id", "nunique")
        )
        .reset_index()
    )

    tab1, tab2 = st.tabs(
        [
            "Best-Selling Products",
            "Slow-Moving Products"
        ]
    )

    
    # BEST SELLING
    

    with tab1:

        best_products = (
            product_summary
            .sort_values(
                "Units_Sold",
                ascending=False
            )
            .head(10)
        )

        st.dataframe(
            best_products,
            use_container_width=True,
            hide_index=True
        )

   
    # SLOW MOVING
    

    with tab2:

        slow_products = (
            product_summary
            .sort_values(
                "Units_Sold",
                ascending=True
            )
            .head(10)
        )

        st.dataframe(
            slow_products,
            use_container_width=True,
            hide_index=True
        )



# PAGE 2: PRODUCT ANALYSIS


elif page == "Product Analysis":

    st.header("Product Analysis")

    st.write(
        "Select a category and product to analyze its demand."
    )

    
    # CATEGORY


    categories = [
        "All Categories"
    ] + sorted(
        products["category"].unique().tolist()
    )

    selected_category = st.selectbox(
        "Category",
        categories
    )

    
    # FILTER PRODUCTS
    

    if selected_category == "All Categories":

        filtered_products = products

    else:

        filtered_products = products[
            products["category"] == selected_category
        ]

    
    # PRODUCT
    

    selected_product = st.selectbox(
        "Product",
        filtered_products["product_id"],
        format_func=lambda x:
            filtered_products.loc[
                filtered_products["product_id"] == x,
                "product_name"
            ].iloc[0]
    )

    
    # PRODUCT DATA
    

    product_data = model_data[
        model_data["product_id"] == selected_product
    ].sort_values("month")

    if len(product_data) > 0:

        first_demand = product_data.iloc[0]["demand"]

        last_demand = product_data.iloc[-1]["demand"]

        
        # DEMAND CHANGE
        

        if first_demand != 0:

            change = (
                (last_demand - first_demand)
                / first_demand
            ) * 100

        else:

            change = 0

        
        # TREND
        

        if change > 10:

            trend = "Increasing"

        elif change < -10:

            trend = "Decreasing"

        else:

            trend = "Stable"

        st.divider()

        # PRODUCT METRICS
        

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Product",
                product_data.iloc[-1]["product_name"]
            )

        with col2:

            st.metric(
                "Latest Demand",
                f"{last_demand:,.0f} units"
            )

        with col3:

            st.metric(
                "Demand Change",
                f"{change:+.1f}%"
            )

        
        # DEMAND TREND
        

        st.subheader("Demand Trend")

        chart_data = (
            product_data[
                ["month", "demand"]
            ]
            .set_index("month")
        )

        st.line_chart(
            chart_data,
            height=350
        )

        
        # CURRENT STATUS
        

        st.subheader("Current Demand Status")

        if trend == "Increasing":

            st.success(
                "Demand is increasing."
            )

        elif trend == "Decreasing":

            st.warning(
                "Demand is decreasing."
            )

        else:

            st.info(
                "Demand is relatively stable."
            )


# PAGE 3: DEMAND PREDICTION


else:

    st.header("Future Demand Prediction")

    st.write(
        "Select a product to estimate its future demand "
        "using recent demand patterns."
    )

    
    # CATEGORY
    

    categories = [
        "All Categories"
    ] + sorted(
        products["category"].unique().tolist()
    )

    selected_category = st.selectbox(
        "Category",
        categories
    )

    
    # FILTER PRODUCTS
    

    if selected_category == "All Categories":

        filtered_products = products

    else:

        filtered_products = products[
            products["category"] == selected_category
        ]

    # PRODUCT

    selected_product = st.selectbox(
        "Product",
        filtered_products["product_id"],
        format_func=lambda x:
            filtered_products.loc[
                filtered_products["product_id"] == x,
                "product_name"
            ].iloc[0]
    )

    # PRODUCT DATA

    product_data = model_data[
        model_data["product_id"] == selected_product
    ].sort_values("month")

    if len(product_data) > 0:

        latest = product_data.iloc[-1]

        # RECENT DEMAND

        st.subheader("Recent Demand")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Last Month",
                f"{latest['lag_1']:.0f} units"
            )

        with col2:

            st.metric(
                "Previous Month",
                f"{latest['lag_2']:.0f} units"
            )

        with col3:

            st.metric(
                "3-Month Average",
                f"{latest['rolling_mean_3']:.0f} units"
            )

        
        
        # RECENT DEMAND CHART

        st.subheader(
            "Recent Demand Trend"
        )

        recent_chart = (
            product_data[
                ["month", "demand"]
            ]
            .tail(12)
            .set_index("month")
        )

        st.line_chart(
            recent_chart,
            height=300
        )

        # PREDICTION
        

        st.subheader("Prediction")

        if st.button(
            "Estimate Future Demand",
            type="primary",
            use_container_width=True
        ):

        
            input_data = pd.DataFrame(
                [{
                    "lag_1": latest["lag_1"],
                    "lag_2": latest["lag_2"],
                    "lag_3": latest["lag_3"],
                    "rolling_mean_3":
                        latest["rolling_mean_3"]
                }]
            )

            prediction = model.predict(
                input_data
            )[0]

            # Demand cannot be negative

            if prediction < 0:

                prediction = 0

            prediction = round(
                prediction
            )

            st.success(
                f"Estimated Future Demand: "
                f"{prediction:,} units"
            )

            st.caption(
                "Prediction is based on recent "
                "historical demand patterns."
            )

# FOOTER
st.divider()

st.caption(
    "E-Commerce Demand Analysis | "
    "Historical Analysis and Demand Prediction"
)