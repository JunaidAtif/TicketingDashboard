import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Support Ticket Dashboard"
    SECRET_KEY: str = os.environ["SECRET_KEY"]
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    DATABASE_URL: str = os.environ["DATABASE_URL"]
    ADMIN_USERNAME: str = os.environ["ADMIN_USERNAME"]
    ADMIN_PASSWORD: str = os.environ["ADMIN_PASSWORD"]

settings = Settings()
