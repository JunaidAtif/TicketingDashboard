from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth.token import Token
from app.services.auth_service import AuthService
from app.api.dependencies import get_auth_service
from app.core.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
