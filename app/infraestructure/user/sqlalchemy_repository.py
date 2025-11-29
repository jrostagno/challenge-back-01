from sqlalchemy.orm import Session

from app.domain.user.repository import UserRepository


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session
