import pandas as pd
from db_connection import engine

def load_excel_to_db():
    try:
        # Load Excel file
        df = pd.read_excel("data/coffee_sales.xlsx", engine="openpyxl")

        # Required columns
        required_columns = [
            "sale_date",
            "sale_datetime",
            "coffee_name",
            "cash_type",
            "money"
        ]

        for col in required_columns:
            if col not in df.columns:
                raise Exception(f"Missing column: {col}")

        # Insert into MySQL
        df.to_sql(
            name="sales",
            con=engine,
            if_exists="append",
            index=False
        )

        print("Data successfully loaded into database!")

    except Exception as e:
        print("ETL Error:", e)


if __name__ == "__main__":
    load_excel_to_db()