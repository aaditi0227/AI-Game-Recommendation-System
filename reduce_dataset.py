import pandas as pd

df = pd.read_csv("dataset/games.csv")

df = df.head(1000)

df.to_csv("dataset/games_1000.csv", index=False)

print("Games:", len(df))
