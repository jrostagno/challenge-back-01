from sqlalchemy.orm import Session

from app.domain.user.entities import User
from app.domain.user.repository import UserRepository
from app.infraestructure.db.models.user_model import UserORM


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user: User) -> User:
        # Domain -> ORM
        orm_user = UserORM(
            user_id=user.user_id,
            name=user.name,
            email=user.email,
            password_hash=user.password_hash,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

        self.session.add(orm_user)
        self.session.commit()
        self.session.refresh(orm_user)

        # ORM -> Domain
        return User(
            user_id=orm_user.user_id,
            name=orm_user.name,
            email=orm_user.email,
            password_hash=orm_user.password_hash,
            created_at=orm_user.created_at,
            updated_at=orm_user.updated_at,
        )
