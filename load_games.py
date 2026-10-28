import pandas as pd
from database import SessionLocal, Game

df = pd.read_csv("dataset/games_1000.csv")

session = SessionLocal()

for _, row in df.iterrows():
    game = Game(
        app_id=row["app_id"],
        title=row["title"],
        date_release=row["date_release"],
        rating=row["rating"],
        positive_ratio=row["positive_ratio"],
        user_reviews=row["user_reviews"],
        price_final=row["price_final"],
        price_original=row["price_original"],
        discount=row["discount"]
    )

    session.add(game)

session.commit()
session.close()

print("1000 games added to SQLite database successfully!")