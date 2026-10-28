from database import SessionLocal, User

session = SessionLocal()

username = input("Enter the username to make admin: ")

user = session.query(User).filter(
    User.username == username
).first()

if user:

    user.is_admin = True

    session.commit()

    print("User is now an admin!")

else:

    print("User not found.")

session.close()
