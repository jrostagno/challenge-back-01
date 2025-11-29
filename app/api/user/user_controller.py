from fastapi import APIRouter
from typing import List
from app.domain.user.entities import User
from app.infraestructure.user.sqlalchemy_repository import SQLAlchemyUserRepository
from app.domain.user.service import UserService
from app.infraestructure.db.session import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends


router = APIRouter(prefix="/users", tags=["users"])


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_services(db:Session=Depends(get_session)):
    repository = SQLAlchemyUserRepository(db)
    return UserService(repository)

# Endpoints

@router.get("/",response_model=List[User],description="List all users")
def list_users(user_service: UserService = Depends(get_user_services)):
    users = user_service.list_users()
    return users