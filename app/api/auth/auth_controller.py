from datetime import timedelta
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.auth.schema import LoginRequest, TokenResponse
from app.domain.user.service import UserService
from app.infraestructure.auth.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
)
from app.infraestructure.db.session import get_session
from app.infraestructure.user.sqlalchemy_repository import SQLAlchemyUserRepository

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


def get_user_service(db: Session = Depends(get_session)) -> UserService:
    repository = SQLAlchemyUserRepository(db)
    return UserService(repository)


@router.post("/login", response_model=TokenResponse)
def login(
    credentials: LoginRequest, user_service: UserService = Depends(get_user_service)
):
    user = user_service.authenticate(
        email=str(credentials.email), password=credentials.password
    )
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={"sub": str(user.user_id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return TokenResponse(access_token=access_token, token_type="bearer")


@router.post("/token", response_model=TokenResponse)
def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service),
):
    user = user_service.authenticate(
        email=form_data.username,  # Swagger usa "username"
        password=form_data.password,
    )
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_access_token(
        data={"sub": str(user.user_id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return TokenResponse(access_token=access_token, token_type="bearer")
