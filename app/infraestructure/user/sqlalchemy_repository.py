from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.domain.user.entities import User
from app.domain.user.exceptions import UserAlreadyExistsError, UserRepositoryError
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

        try:
            self.session.add(orm_user)
            self.session.commit()

        except IntegrityError as e:
            self.session.rollback()
            raise UserAlreadyExistsError(
                f"User with email {user.email} already exists"
            ) from e

        except SQLAlchemyError as e:
            self.session.rollback()
            raise UserRepositoryError(f"User repository error: {e}") from e

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

    def get_user_by_email(self, email: str) -> User | None:

        try:
            orm_user = (
                self.session.query(UserORM).filter(UserORM.email == email).first()
            )

        except IntegrityError as e:
            raise UserRepositoryError(f"User repository error: {e}") from e

        if not orm_user:
            return None

        return User(
            user_id=orm_user.user_id,
            name=orm_user.name,
            email=orm_user.email,
            password_hash=orm_user.password_hash,
            created_at=orm_user.created_at,
            updated_at=orm_user.updated_at,
        )
