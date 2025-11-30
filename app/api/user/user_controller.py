from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.user.schemas import UserCreate, UserResponse
from app.domain.user.entities import User
from app.domain.user.service import UserService
from app.infraestructure.db.session import SessionLocal
from app.infraestructure.user.sqlalchemy_repository import SQLAlchemyUserRepository

router = APIRouter(prefix="/users", tags=["users"])


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_services(db: Session = Depends(get_session)):
    repository = SQLAlchemyUserRepository(db)
    return UserService(repository)


# Endpoints
@router.post("/", response_model=UserResponse, description="Create a new user")
def create_user(
    user_in: UserCreate, user_service: UserService = Depends(get_user_services)
):

    now = datetime.now()

    user_entity = User(
        name=user_in.name,
        email=str(user_in.email),
        password_hash=user_in.password,
        created_at=now,
        updated_at=now,
    )

    created_user = user_service.create_user(user_entity)

    return UserResponse.model_validate(created_user)
