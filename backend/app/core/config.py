import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Support Ticket Dashboard"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-that-should-be-in-env")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "agent")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "password123")

settings = Settings()
