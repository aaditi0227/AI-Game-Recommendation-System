from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from database import SessionLocal, Game, User, Wishlist


app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="game-recommendation-secret-key"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

df = pd.read_csv("dataset/games_1000.csv")

df["title"] = df["title"].fillna("")
df["rating"] = df["rating"].fillna("")
df["positive_ratio"] = df["positive_ratio"].fillna(0)
df["user_reviews"] = df["user_reviews"].fillna(0)
df["price_final"] = df["price_final"].fillna(0)

df["features"] = (
    df["title"] + " " +
    df["rating"].astype(str) + " " +
    df["positive_ratio"].astype(str)
)

vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(df["features"])
similarity = cosine_similarity(tfidf_matrix)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    username = request.session.get("username")

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "username": username
        }
    )


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )


@app.post("/register", response_class=HTMLResponse)
def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    session = SessionLocal()

    existing_user = session.query(User).filter(
        (User.username == username) |
        (User.email == email)
    ).first()

    if existing_user:
        session.close()

        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "message": "Username or email already exists."
            }
        )

    if password != confirm_password:
        session.close()

        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "message": "Passwords do not match."
            }
        )

    new_user = User(
        username=username,
        email=email,
        password=password
    )

    session.add(new_user)
    session.commit()
    session.close()

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "message": "Registration successful! You can now login."
        }
    )


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@app.post("/login", response_class=HTMLResponse)
def login_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    session = SessionLocal()

    user = session.query(User).filter(
        User.username == username,
        User.password == password
    ).first()

    session.close()

    if user:
        request.session["username"] = user.username
        request.session["user_id"] = user.id

        return RedirectResponse(
            url="/",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "message": "Invalid username or password."
        }
    )


@app.get("/logout")
def logout(request: Request):
    request.session.clear()

    return RedirectResponse(
        url="/",
        status_code=303
    )


@app.get("/search/{game_name}")
def search_games(game_name: str):
    session = SessionLocal()

    results = session.query(Game).filter(
        Game.title.ilike(f"%{game_name}%")
    ).limit(10).all()

    session.close()

    return {
        "results": [
            game.title
            for game in results
        ]
    }


@app.get("/recommend/{game_name}")
def recommend_games(game_name: str):
    matches = df[
        df["title"].str.lower() == game_name.lower()
    ]

    if matches.empty:
        return {
            "message": "Game not found"
        }

    index = matches.index[0]

    scores = list(enumerate(similarity[index]))

    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    for i, score in scores[1:6]:
        game = df.iloc[i]

        recommendations.append({
            "title": str(game["title"]),
            "rating": str(game["rating"]),
            "positive_ratio": int(game["positive_ratio"]),
            "user_reviews": int(game["user_reviews"]),
            "price": float(game["price_final"])
        })

    return {
        "game": str(df.iloc[index]["title"]),
        "recommendations": recommendations
    }


@app.get("/wishlist", response_class=HTMLResponse)
def wishlist_page(request: Request):
    username = request.session.get("username")
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    session = SessionLocal()

    wishlist = session.query(Wishlist).filter(
        Wishlist.user_id == user_id
    ).all()

    session.close()

    return templates.TemplateResponse(
        request=request,
        name="wishlist.html",
        context={
            "username": username,
            "wishlist": wishlist
        }
    )


@app.post("/wishlist/add")
def add_to_wishlist(
    request: Request,
    game_title: str = Form(...)
):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    session = SessionLocal()

    game = session.query(Game).filter(
        Game.title == game_title
    ).first()

    if game:
        existing = session.query(Wishlist).filter(
            Wishlist.user_id == user_id,
            Wishlist.game_id == game.id
        ).first()

        if not existing:
            wishlist_item = Wishlist(
                user_id=user_id,
                game_id=game.id,
                game_title=game.title
            )

            session.add(wishlist_item)
            session.commit()

    session.close()

    return RedirectResponse(
        url="/wishlist",
        status_code=303
    )


@app.post("/wishlist/remove/{wishlist_id}")
def remove_from_wishlist(
    request: Request,
    wishlist_id: int
):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    session = SessionLocal()

    item = session.query(Wishlist).filter(
        Wishlist.id == wishlist_id,
        Wishlist.user_id == user_id
    ).first()

    if item:
        session.delete(item)
        session.commit()

    session.close()

    return RedirectResponse(
        url="/wishlist",
        status_code=303
    )


@app.get("/profile", response_class=HTMLResponse)
def profile_page(request: Request):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    session = SessionLocal()

    user = session.query(User).filter(
        User.id == user_id
    ).first()

    wishlist = session.query(Wishlist).filter(
        Wishlist.user_id == user_id
    ).all()

    wishlist_count = len(wishlist)

    session.close()

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            "user": user,
            "wishlist": wishlist,
            "wishlist_count": wishlist_count
        }
    )


@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    session = SessionLocal()

    user = session.query(User).filter(
        User.id == user_id
    ).first()

    if not user or not user.is_admin:
        session.close()

        return HTMLResponse(
            content="""
            <html>
            <head>
                <title>Access Denied</title>
            </head>
            <body>
                <h1>🚫 Access Denied</h1>
                <p>You do not have administrator permissions.</p>
                <a href="/">Go to Home</a>
            </body>
            </html>
            """,
            status_code=403
        )

    total_users = session.query(User).count()
    total_games = session.query(Game).count()
    total_wishlist = session.query(Wishlist).count()

    users = session.query(User).all()
    games = session.query(Game).limit(50).all()

    session.close()

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "username": user.username,
            "total_users": total_users,
            "total_games": total_games,
            "total_wishlist": total_wishlist,
            "users": users,
            "games": games
        }
    )


@app.get("/admin/add-game", response_class=HTMLResponse)
def add_game_page(request: Request):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    session = SessionLocal()

    user = session.query(User).filter(
        User.id == user_id
    ).first()

    if not user or not user.is_admin:
        session.close()

        return HTMLResponse(
            content="""
            <h1>🚫 Access Denied</h1>
            <a href="/">Go to Home</a>
            """,
            status_code=403
        )

    session.close()

    return templates.TemplateResponse(
        request=request,
        name="add_game.html",
        context={}
    )


@app.post("/admin/add-game")
def add_game(
    request: Request,
    app_id: int = Form(...),
    title: str = Form(...),
    date_release: str = Form(""),
    rating: str = Form(""),
    positive_ratio: int = Form(0),
    user_reviews: int = Form(0),
    price_final: float = Form(0),
    price_original: float = Form(0),
    discount: float = Form(0)
):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    session = SessionLocal()

    user = session.query(User).filter(
        User.id == user_id
    ).first()

    if not user or not user.is_admin:
        session.close()

        return HTMLResponse(
            content="""
            <h1>🚫 Access Denied</h1>
            <a href="/">Go to Home</a>
            """,
            status_code=403
        )

    existing_game = session.query(Game).filter(
        Game.app_id == app_id
    ).first()

    if existing_game:
        session.close()

        return HTMLResponse(
            content="""
            <h1>⚠️ Game Already Exists</h1>
            <p>A game with this App ID already exists.</p>
            <a href="/admin">Back to Admin Dashboard</a>
            """,
            status_code=400
        )

    new_game = Game(
        app_id=app_id,
        title=title,
        date_release=date_release,
        rating=rating,
        positive_ratio=positive_ratio,
        user_reviews=user_reviews,
        price_final=price_final,
        price_original=price_original,
        discount=discount
    )

    session.add(new_game)
    session.commit()
    session.close()

    return RedirectResponse(
        url="/admin",
        status_code=303
    )


@app.post("/admin/delete-game/{game_id}")
def delete_game(
    request: Request,
    game_id: int
):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    session = SessionLocal()

    user = session.query(User).filter(
        User.id == user_id
    ).first()

    if not user or not user.is_admin:
        session.close()

        return HTMLResponse(
            content="""
            <h1>🚫 Access Denied</h1>
            <a href="/">Go to Home</a>
            """,
            status_code=403
        )

    game = session.query(Game).filter(
        Game.id == game_id
    ).first()

    if game:
        session.delete(game)
        session.commit()

    session.close()

    return RedirectResponse(
        url="/admin",
        status_code=303
    )
@app.post("/admin/delete-user/{user_id}")
def delete_user(
    request: Request,
    user_id: int
):

    admin_id = request.session.get("user_id")

    if not admin_id:

        return RedirectResponse(
            url="/login",
            status_code=303
        )

    session = SessionLocal()

    admin = session.query(User).filter(
        User.id == admin_id
    ).first()

    if not admin or not admin.is_admin:

        session.close()

        return HTMLResponse(
            content="""
            <h1>🚫 Access Denied</h1>
            <a href="/">Go to Home</a>
            """,
            status_code=403
        )

    user = session.query(User).filter(
        User.id == user_id
    ).first()

    if user:

        if user.id == admin_id:

            session.close()

            return HTMLResponse(
                content="""
                <h1>⚠️ Cannot Delete Yourself</h1>
                <p>You cannot delete your own administrator account.</p>
                <a href="/admin">Back to Admin Dashboard</a>
                """
            )

        session.query(Wishlist).filter(
            Wishlist.user_id == user.id
        ).delete()

        session.delete(user)

        session.commit()

    session.close()

    return RedirectResponse(
        url="/admin",
        status_code=303
    )