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

date=r"[0-9][0-9]/[0-9][0-9]/[0-9][0-9]"
name=r"(.*?)"
item=r"(.*?)"
price=r"([0-9,]+)"

pattern = (
    rf"({date}),.*?-\s"
    rf"{name}:\s"
    rf"{item}\s+"
    rf"{price}$"
)

matches = re.findall(pattern, data, re.MULTILINE)

#3.csv
df = pd.DataFrame(matches, columns=["date","name","item", "price"])
df["date"] = pd.to_datetime(
    df["date"],
    format="%d/%m/%y"
).dt.strftime("%d-%m-%Y")
df["price"] = df["price"].astype(int)
df.to_excel("expenses.xlsx", index=False)
m_total=df["price"].sum()
print("monthly total:",m_total)
