#1.uploading the exported chat 
from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw() # Hide the main Tkinter window

file_path = askopenfilename(
    title="Select WhatsApp Chat Export",
    filetypes=[("Text Files", "*.txt")]
)

with open(file_path, "r", encoding="utf-8") as file:
    data = file.read()

#2.RE
import re
import pandas as pd
message_pattern = (
    r"([0-9]{2}/[0-9]{2}/[0-9]{2}),.*?-\s"
    r"(.*?):\s"
    r"([\s\S]*?)"
    r"(?=\n[0-9]{2}/[0-9]{2}/[0-9]{2},|\Z)"
)

messages = re.findall(message_pattern, data)

expenses = []

for date, name, message in messages:

    lines = message.split("\n")

    for line in lines:

        match = re.search(r"(.*)\s([0-9,]+)$", line)

        if match:

            item = match.group(1).strip()
            price = match.group(2)

            expenses.append([date, name, item, price])

#3.csv
df = pd.DataFrame(expenses, columns=["date","name","item", "price"])
df["date"] = pd.to_datetime(
    df["date"],
    format="%d/%m/%y"
)

#, error
df["price"] = df["price"].str.replace(",", "").astype(int)
df.to_excel("expenses.xlsx", index=False)

#monthwise
month= int(input("Enter month (1-12): "))
month_df= df[df["date"].dt.month == month]

print(month_df)
print("Entries:", len(month_df))

m_total=month_df["price"].sum()
print("monthly total:",m_total)
