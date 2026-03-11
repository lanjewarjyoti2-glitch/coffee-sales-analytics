import pandas as pd

data = {
    "date": [
        "2026-02-15",
        "2026-02-16",
        "2026-02-17",
        "2026-02-18",
        "2026-02-19"
    ],
    "datetime": [
        "09:15",
        "10:10",
        "11:30",
        "12:20",
        "14:05"
    ],
    "cash_type": [
        "Cash",
        "Card",
        "Cash",
        "Card",
        "Cash"
    ],
    "card": [
        0,
        1,
        0,
        1,
        0
    ],
    "money": [
        150,
        210,
        180,
        220,
        250
    ],
    "coffee_name": [
        "Latte",
        "Cappuccino",
        "Espresso",
        "Americano",
        "Cocoa"
    ]
}

df = pd.DataFrame(data)

df.to_excel("testing_report.xlsx", index=False)

print("Excel file created: testing_report.xlsx")