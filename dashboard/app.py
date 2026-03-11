import streamlit as st
import pandas as pd
import mysql.connector
import joblib
from datetime import timedelta


# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="coffee_sales_db"
    )


# -----------------------------------
# LOAD DATA
# -----------------------------------
def load_data():
    conn = get_connection()
    query = "SELECT sale_date, coffee_name, money FROM sales"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# -----------------------------------
# FORECAST FUNCTION
# -----------------------------------
def generate_forecast():
    conn = get_connection()

    model = joblib.load("src/sales_model.pkl")

    df = pd.read_sql("SELECT sale_date FROM sales", conn)
    df["sale_date"] = pd.to_datetime(df["sale_date"])

    last_date = df["sale_date"].max()

    future_dates = []
    future_day_numbers = []

    for i in range(1, 8):
        next_date = last_date + timedelta(days=i)
        future_dates.append(next_date)
        future_day_numbers.append(next_date.toordinal())

    future_df = pd.DataFrame({
        "sale_date": future_dates,
        "day_number": future_day_numbers
    })

    future_df["predicted_sales"] = model.predict(
        future_df[["day_number"]]
    )

    conn.close()
    return future_df


# -----------------------------------
# STREAMLIT UI
# -----------------------------------
st.title("☕ Coffee Sales Dashboard")

df = load_data()

if df.empty:
    st.error("No data found in sales table.")
else:
    df["sale_date"] = pd.to_datetime(df["sale_date"])

    # ----------------------------
    # BUSINESS SUMMARY SECTION
    # ----------------------------
    total_revenue = df["money"].sum()
    total_orders = len(df)
    top_coffee = df.groupby("coffee_name")["money"].sum().idxmax()

    st.subheader("📌 Business Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"₹{total_revenue}")
    col2.metric("Total Orders", total_orders)
    col3.metric("Top Coffee", top_coffee)

    # ----------------------------
    # HISTORICAL SALES CHART
    # ----------------------------
    st.subheader("📊 Historical Sales")
    st.line_chart(df.set_index("sale_date")["money"])

    # ----------------------------
    # FORECAST SECTION
    # ----------------------------
    st.subheader("📈 7-Day Sales Forecast")

    try:
        forecast_df = generate_forecast()
        st.line_chart(
            forecast_df.set_index("sale_date")["predicted_sales"]
        )
        st.dataframe(forecast_df)

    except Exception as e:
        st.error(f"Forecast error: {e}")