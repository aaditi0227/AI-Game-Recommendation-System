import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("dataset/games_1000.csv")

df["title"] = df["title"].fillna("")
df["rating"] = df["rating"].fillna("")
df["positive_ratio"] = df["positive_ratio"].fillna(0)
df["user_reviews"] = df["user_reviews"].fillna(0)

df["features"] = (
    df["title"] + " " +
    df["rating"].astype(str) + " " +
    df["positive_ratio"].astype(str)
)

vectorizer = TfidfVectorizer(stop_words="english")

tfidf_matrix = vectorizer.fit_transform(df["features"])

similarity = cosine_similarity(tfidf_matrix)


def recommend_games(game_name, n=5):

    matches = df[
        df["title"].str.lower() == game_name.lower()
    ]

    if matches.empty:
        return ["Game not found"]

    index = matches.index[0]

    scores = list(enumerate(similarity[index]))

    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    for i, score in scores[1:n+1]:
        recommendations.append(df.iloc[i]["title"])

    return recommendations


game = input("Enter a game name: ")

print("\nRecommended Games:")

for game in recommend_games(game):
    print("-", game)