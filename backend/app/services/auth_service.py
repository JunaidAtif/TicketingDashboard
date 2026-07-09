from app.repositories.user_repository import UserRepository
from app.core.security import verify_password
from app.core.exceptions import CredentialsException
from app.models.user import User

class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def authenticate_user(self, username: str, password: str) -> User:
        user = self.repository.get_by_username(username)
        if not user:
            raise CredentialsException()
        if not verify_password(password, user.hashed_password):
            raise CredentialsException()
        return user
