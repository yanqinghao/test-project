import random
import sqlite3
import pandas as pd

df = pd.read_excel("private/表格1.xlsx", index_col=0)
print(df)

cnx = sqlite3.connect("private/2-100.db")
df1 = pd.read_sql("SELECT * FROM data", cnx)
print(df1)

df1["simple_content"] = df1["content"].str.replace("<.+?>", " ")
classes = ["simulation", "hardware", "edge_computing"]
df1["label"] = random.choices(classes, k=len(df1))
df1.to_sql(name="data", con=cnx, index=False, if_exists='replace')
df1.to_csv("private/2-100.csv", index=False)
