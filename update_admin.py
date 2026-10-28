
from sqlalchemy import inspect, text
from database import engine

inspector = inspect(engine)

columns = [
    column["name"]
    for column in inspector.get_columns("users")
]

if "is_admin" not in columns:
    with engine.begin() as connection:
        connection.execute(
            text(
                "ALTER TABLE users "
                "ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0"
            )
        )

    print("Admin role column added successfully!")
else:
    print("Admin role column already exists.")