from app.infraestructure.db.base import Base
from sqlalchemy import Column, Integer, String, DateTime, UUID
from datetime import datetime

class UserORM(Base):
    __tablename__ = "users"
    id=Mapped[int] = Column(Integer, primary_key=True, index=True)
    name=Mapped[str] = Column(String, index=True)
    email=Mapped[str] = Column(String, unique=True, index=True)
    password=Mapped[str] = Column(String)
    created_at=Mapped[datetime] = Column(DateTime, default=datetime.now)
    updated_at=Mapped[datetime] = Column(DateTime, default=datetime.now)