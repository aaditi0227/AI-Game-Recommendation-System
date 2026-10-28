
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./game_recommendation.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

Base = declarative_base()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    app_id = Column(Integer)
    title = Column(String)
    date_release = Column(String)
    rating = Column(String)
    positive_ratio = Column(Integer)
    user_reviews = Column(Integer)
    price_final = Column(Float)
    price_original = Column(Float)
    discount = Column(Float)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)


class Wishlist(Base):
    __tablename__ = "wishlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    game_id = Column(Integer)
    game_title = Column(String)


Base.metadata.create_all(bind=engine)

print("SQLite database initialized successfully!")