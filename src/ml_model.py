import pandas as pd
import mysql.connector
import joblib
from datetime import timedelta
from sklearn.linear_model import LinearRegression


# -----------------------------
# DATABASE CONNECTION (MySQL)
# -----------------------------
def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",        # change if needed
        password="",        # add password if you set one
        database="coffee_sales_db"  # your phpMyAdmin database name
    )
    return conn


# -----------------------------
# TRAIN MODEL
# -----------------------------
def train_model():
    conn = get_connection()

    query = "SELECT sale_date, money FROM sales"
    df = pd.read_sql(query, conn)

    df["sale_date"] = pd.to_datetime(df["sale_date"])
    df["day_number"] = df["sale_date"].map(pd.Timestamp.toordinal)

    X = df[["day_number"]]
    y = df["money"]

    model = LinearRegression()
    model.fit(X, y)

    joblib.dump(model, "src/sales_model.pkl")

    print("✅ Model trained successfully.")

    conn.close()


# -----------------------------
# PREDICT NEXT 7 DAYS
# -----------------------------
def predict_next_7_days():
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

    future_df["predicted_sales"] = model.predict(future_df[["day_number"]])

    conn.close()

    return future_df


# -----------------------------
# RUN FILE
# -----------------------------
if __name__ == "__main__":
    train_model()
    forecast = predict_next_7_days()
    print("\n📊 Next 7 Days Forecast:\n")
    print(forecast)