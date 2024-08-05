import pandas as pd
import sys
import os

# Ajustar la ruta para que apunte correctamente al directorio 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from hacker_news_table_extracter import time_to_hour 

df = pd.read_csv("../data/hacker_news_news_20240805.csv")
df[["num", "long", "ot"]] = df["time"].str.split(" ", expand=True)

# apply time_to_hour function to the time column time
df["time_hour"] = df.apply(lambda row: time_to_hour(row, "20240805"), axis=1)

print(df[["time","time_hour"]].head())
