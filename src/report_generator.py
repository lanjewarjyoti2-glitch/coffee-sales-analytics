import pandas as pd
from db_connection import engine


def generate_report():
    # Total Revenue
    total_revenue_query = "SELECT SUM(money) AS total_revenue FROM sales;"
    total_revenue = pd.read_sql(total_revenue_query, engine)

    # Best Selling Coffee
    best_selling_query = """
    SELECT coffee_name, COUNT(*) AS total_sales
    FROM sales
    GROUP BY coffee_name
    ORDER BY total_sales DESC;
    """
    best_selling = pd.read_sql(best_selling_query, engine)

    # Payment Analysis
    payment_query = """
    SELECT cash_type, SUM(money) AS revenue
    FROM sales
    GROUP BY cash_type;
    """
    payment_analysis = pd.read_sql(payment_query, engine)

    # Daily Trend
    daily_query = """
    SELECT sale_date, SUM(money) AS daily_revenue
    FROM sales
    GROUP BY sale_date
    ORDER BY sale_date;
    """
    daily_trend = pd.read_sql(daily_query, engine)

    # Save to Excel
    with pd.ExcelWriter("reports/generated_report.xlsx") as writer:
        total_revenue.to_excel(writer, sheet_name="Total Revenue", index=False)
        best_selling.to_excel(writer, sheet_name="Best Selling Coffee", index=False)
        payment_analysis.to_excel(writer, sheet_name="Payment Analysis", index=False)
        daily_trend.to_excel(writer, sheet_name="Daily Sales Trend", index=False)

    print("Report successfully generated!")


if __name__ == "__main__":
    generate_report()