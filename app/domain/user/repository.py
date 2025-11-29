from abc import ABC, abstractmethod
from typing import List

from pydantic import EmailStr

from app.domain.user.entities import User


class UserRepository(ABC):

    @abstractmethod
    def list_users(self) -> List[User]:
        pass

    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_user_by_id(self, id: int) -> User:
        pass

    @abstractmethod
    def get_user_by_email(self, email: EmailStr) -> User:
        pass
