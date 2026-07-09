from app.database.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def seed():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == "agent").first()
        if not user:
            print("Creating default 'agent' user...")
            hashed_password = get_password_hash("password123")
            new_user = User(username="agent", hashed_password=hashed_password, role="agent")
            db.add(new_user)
            db.commit()
            print("User created successfully!")
        else:
            print("User 'agent' already exists.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
