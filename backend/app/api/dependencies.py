from typing import Generator
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.database.session import SessionLocal
from app.core.config import settings
from app.core.exceptions import CredentialsException
from app.repositories.user_repository import UserRepository
from app.repositories.ticket_repository import TicketRepository
from app.services.auth_service import AuthService
from app.services.ticket_service import TicketService
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")
""
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_ticket_repository(db: Session = Depends(get_db)) -> TicketRepository:
    return TicketRepository(db)

def get_auth_service(repository: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(repository)

def get_ticket_service(repository: TicketRepository = Depends(get_ticket_repository)) -> TicketService:
    return TicketService(repository)

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    repository: UserRepository = Depends(get_user_repository)
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException()
    except JWTError:
        raise CredentialsException()
        
    user = repository.get_by_username(username)
    if user is None:
        raise CredentialsException()
    return user
