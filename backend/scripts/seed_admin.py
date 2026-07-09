from app.database.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash
from app.core.config import settings

def seed():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
        if not user:
            print(f"Creating default '{settings.ADMIN_USERNAME}' user...")
            hashed_password = get_password_hash(settings.ADMIN_PASSWORD)
            new_user = User(username=settings.ADMIN_USERNAME, hashed_password=hashed_password, role="agent")
            db.add(new_user)
            db.commit()
            print("User created successfully!")
        else:
            print(f"User '{settings.ADMIN_USERNAME}' already exists.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
