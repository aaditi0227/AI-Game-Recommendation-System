# AI Game Recommendation System

A Python web application that helps users discover games through content-based recommendations. It uses TF-IDF vectorization and cosine similarity to compare game attributes and return similar titles.

## Features

- Content-based game recommendations
- Game search
- User registration and login
- Personal wishlist
- Profile page
- Admin dashboard and game management
- HTML/CSS interface rendered with Jinja2 templates

## Tech Stack

- **Language:** Python
- **Web framework:** FastAPI
- **Data processing:** Pandas
- **Recommendation algorithm:** Scikit-learn (TF-IDF and cosine similarity)
- **Database:** SQLite with SQLAlchemy
- **Templates:** Jinja2
- **Frontend:** HTML and CSS

## How Recommendations Work

1. The application reads game information from `dataset/games_1000.csv`.
2. It prepares features from each game's title, rating, and positive review ratio.
3. TF-IDF converts those text features into numerical vectors.
4. Cosine similarity compares the vectors.
5. The system returns the five highest-ranked similar titles for a selected game.

## Project Structure

```text
AI-Game-Recommendation-System/
├── dataset/
│   ├── games.csv
│   └── games_1000.csv
├── static/
│   └── style.css
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   ├── wishlist.html
│   ├── admin.html
│   └── add_game.html
├── main.py
├── recommendation.py
├── database.py
├── load_games.py
├── check_dataset.py
├── reduce_dataset.py
├── make_admin.py
├── update_admin.py
├── requirements.txt
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.10 or later
- pip

### 1. Clone the repository

```bash
git clone https://github.com/aaditi0227/AI-Game-Recommendation-System.git
cd AI-Game-Recommendation-System
```

### 2. Create and activate a virtual environment

On Windows:

```bash
python -m venv venv
venv\\Scripts\\activate
```

On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize the database and load games

```bash
python database.py
python load_games.py
```

Run the game-loading script only when populating a fresh database; running it repeatedly may add duplicate records.

### 5. Run the web application

```bash
uvicorn main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Notes

- The app expects the dataset file at `dataset/games_1000.csv`.
- The SQLite database is created locally by `database.py`.
- For a real deployment, configure a secure session secret outside the source code and use secure password handling before exposing the app publicly.

## Author

**Aaditi Apale**  
GitHub: [@aaditi0227](https://github.com/aaditi0227)
