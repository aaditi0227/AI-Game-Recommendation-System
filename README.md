# AI Game Recommendation System 🎮

## Overview

The **AI Game Recommendation System** is a Python-based web application that recommends similar games based on game titles, ratings, and positive review ratios. It uses Natural Language Processing (NLP) techniques and a content-based filtering approach to identify similarities between games and provide personalized discovery options.

The application also includes user registration, login, game search, wishlist management, and an administrative interface.

## Features

- **Game Recommendations:** Recommends similar games using TF-IDF vectorization and cosine similarity.
- **Game Search:** Search for games by title.
- **User Authentication:** Register an account, log in, and log out.
- **Wishlist Management:** Save and manage games of interest.
- **Admin Interface:** Includes an administrative section for game management.
- **Game Dataset:** Uses a dataset containing game information, ratings, reviews, and pricing.
- **Web Interface:** Provides an interactive interface built with HTML, CSS, and Jinja2 templates.

## Technologies Used

- **Programming Language:** Python
- **Web Framework:** FastAPI
- **Machine Learning / NLP:** Scikit-learn, TF-IDF, Cosine Similarity
- **Data Processing:** Pandas
- **Database:** SQLite, SQLAlchemy
- **Frontend:** HTML, CSS, Jinja2 Templates
- **Session Management:** Starlette Session Middleware

## How It Works

1. The system loads game information from a CSV dataset.
2. It preprocesses selected game attributes, including titles, ratings, and positive review ratios.
3. TF-IDF converts the combined text features into numerical vectors.
4. Cosine similarity calculates how closely games match one another.
5. When a user selects a game, the system returns other games with the highest similarity scores.

## Project Structure

```text
AI-Game-Recommendation-System/
│
├── dataset/
│   ├── games.csv
│   └── games_1000.csv
│
├── static/
│   └── style.css
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   ├── wishlist.html
│   ├── admin.html
│   └── add_game.html
│
├── main.py
├── recommendation.py
├── database.py
├── load_games.py
├── check_dataset.py
├── reduce_dataset.py
├── make_admin.py
└── update_admin.py
```

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- pip

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
```

Replace the URL with your actual GitHub repository URL.

### 2. Navigate to the project directory

```bash
cd AI-Game-Recommendation-System
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install the dependencies

```bash
pip install fastapi uvicorn pandas scikit-learn sqlalchemy jinja2 python-multipart itsdangerous
```

### 5. Initialize the database

```bash
python database.py
```

### 6. Load the game dataset

```bash
python load_games.py
```

Run the database initialization and data-loading steps only when setting up a fresh database, to avoid duplicate game records.

### 7. Start the application

```bash
uvicorn main:app --reload
```

Open the following URL in your browser:

`http://127.0.0.1:8000`

## Recommendation Algorithm

The project uses a content-based recommendation approach.

- **TF-IDF Vectorization:** Converts selected game attributes into numerical feature vectors.
- **Cosine Similarity:** Measures similarity between game vectors.
- **Ranking:** Sorts games by similarity and returns the top matching recommendations.

This approach helps users discover games with similar characteristics without requiring collaborative user-rating data.

## Learning Outcomes

- Implementing a content-based recommendation system.
- Applying NLP techniques to structured game information.
- Building a web application using FastAPI.
- Integrating SQLite with SQLAlchemy.
- Working with CSV datasets using Pandas.
- Connecting recommendation logic with a user-facing web interface.

## Future Improvements

- Incorporate game genres, descriptions, and tags into recommendations.
- Add advanced filtering by price, rating, and category.
- Improve password security and session configuration.
- Introduce user-preference-based recommendations.
- Deploy the application to a cloud platform.

## Author

**Aaditi Apale**

GitHub: [@aaditi0227](https://github.com/aaditi0227)

---

If you find this project useful, feel free to explore the repository and suggest improvements.
