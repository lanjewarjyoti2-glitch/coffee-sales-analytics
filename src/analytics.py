import pandas as pd
from db_connection import engine

def total_revenue():
    query = "SELECT SUM(money) AS total_revenue FROM sales;"
    df = pd.read_sql(query, engine)
    print("Total Revenue:", df["total_revenue"][0])


def best_selling_coffee():
    query = """
    SELECT coffee_name, COUNT(*) AS total_sales
    FROM sales
    GROUP BY coffee_name
    ORDER BY total_sales DESC
    LIMIT 1;
    """
    df = pd.read_sql(query, engine)
    print("Best Selling Coffee:")
    print(df)


def payment_analysis():
    query = """
    SELECT cash_type, SUM(money) AS revenue
    FROM sales
    GROUP BY cash_type;
    """
    df = pd.read_sql(query, engine)
    print("Revenue by Payment Type:")
    print(df)


def daily_sales_trend():
    query = """
    SELECT sale_date, SUM(money) AS daily_revenue
    FROM sales
    GROUP BY sale_date
    ORDER BY sale_date;
    """
    df = pd.read_sql(query, engine)
    print("Daily Sales Trend:")
    print(df)


if __name__ == "__main__":
    total_revenue()
    best_selling_coffee()
    payment_analysis()
    daily_sales_trend()