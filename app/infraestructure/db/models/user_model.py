from app.infraestructure.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import  Integer, String, DateTime, UUID
from datetime import datetime

class UserORM(Base):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name:Mapped[str] = mapped_column(String, index=True)
    email:Mapped[str] = mapped_column(String, unique=True, index=True)
    password:Mapped[str] = mapped_column(String)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now)