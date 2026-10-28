import pandas as pd

df = pd.read_csv("dataset/games.csv")

print("Number of games:", len(df))
print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())