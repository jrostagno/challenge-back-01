from app.domain.user.repository import UserRepository
from app.domain.user.entities import User
from app.infraestructure.db.models.user_model import UserORM
from sqlalchemy.orm import Session
from typing import List

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def list_users(self)->List[User]:
        return self.session.query(UserORM).all()