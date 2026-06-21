import re
import pandas as pd


# -----------------------------
# READ WHATSAPP FILE
# -----------------------------

file = open(
    r"C:\Users\saeeh\Downloads\WhatsApp Chat with Monthly expenses 💸💰.txt",
    encoding="utf-8"
)

data = file.readlines()


# -----------------------------
# PARSE EXPENSES
# -----------------------------

pattern = r"(\d+/\d+/\d+).*? - (.*?): (.*)"

expenses = []

for line in data:

    match = re.match(pattern, line)

    if match:

        date = match.group(1)
        person = match.group(2)
        message = match.group(3)

        # ignore deleted/random messages
        if "deleted" in message.lower():
            continue


        amount = re.findall(
            r"\d+(?:\.\d+)?",
            message
        )

        if amount:

            price = amount[-1]

            item = (
                message
                .replace(price, "")
                .strip()
            )

            expenses.append(
                [
                    date,
                    person,
                    item,
                    float(price)
                ]
            )


# -----------------------------
# CREATE DATAFRAME
# -----------------------------

df = pd.DataFrame(
    expenses,
    columns=[
        "Date",
        "Person",
        "Expense",
        "Amount"
    ]
)


# convert date column

df["Date"] = pd.to_datetime(
    df["Date"],
    format="%d/%m/%y"
)


# -----------------------------
# FILTER APRIL ONLY
# -----------------------------

april_df = df[
    df["Date"].dt.month == 4
]


# -----------------------------
# APRIL TOTAL
# -----------------------------

total = april_df["Amount"].sum()

print("-----------------------")
print("APRIL EXPENSE SUMMARY")
print("-----------------------")

print(april_df)

print()

print(
    "Total April Expense = ₹",
    total
)


# -----------------------------
# SAVE EXCEL
# -----------------------------

output_path = r"C:\Users\saeeh\Downloads\April_expenses.xlsx"

with pd.ExcelWriter(output_path) as writer:

    april_df.to_excel(
        writer,
        sheet_name="April Expenses",
        index=False
    )

    april_df.groupby(
        "Person"
    )["Amount"].sum().to_excel(
        writer,
        sheet_name="Person Summary"
    )


print()
print("Excel created 💸")
print("Saved at:", output_path)