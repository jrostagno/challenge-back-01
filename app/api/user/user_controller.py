from fastapi import APIRouter

from app.infraestructure.db.session import SessionLocal

router = APIRouter(prefix="/users", tags=["users"])


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# def get_user_services(db:Session=Depends(get_session)):
#     repository = SQLAlchemyUserRepository(db)
#     return UserService(repository)

# Endpoints
