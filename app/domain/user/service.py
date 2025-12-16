from datetime import UTC, datetime

from app.domain.user.entities import User
from app.domain.user.repository import UserRepository
from app.infraestructure.auth.security import hash_password, verify_password


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user_with_password(self, name: str, email: str, password: str) -> User:
        password_hash = hash_password(password)

        user = User(
            name=name,
            email=email,
            password_hash=password_hash,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        return self.user_repository.create_user(user)

    def authenticate(self, email: str, password: str) -> User | None:
        user = self.user_repository.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user
