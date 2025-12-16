from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.user.schemas import UserCreate, UserResponse
from app.domain.user.entities import User
from app.domain.user.service import UserService
from app.infraestructure.db.session import get_session
from app.infraestructure.user.sqlalchemy_repository import SQLAlchemyUserRepository

router = APIRouter(prefix="/users", tags=["users"])

_DEFAULT_SESSION_DEPENDENCY = Depends(get_session)


def get_user_services(db: Session = _DEFAULT_SESSION_DEPENDENCY):
    repository = SQLAlchemyUserRepository(db)
    return UserService(repository)


_DEFAULT_USER_SERVICE_DEPENDENCY = Depends(get_user_services)


# Endpoints
@router.post("/", response_model=UserResponse, description="Create a new user")
def create_user(
    user_in: UserCreate, user_service: UserService = _DEFAULT_USER_SERVICE_DEPENDENCY
):

    user: User = user_service.create_user_with_password(
        name=user_in.name, email=str(user_in.email), password=user_in.password
    )

    return UserResponse.model_validate(user)
