from fastapi import FastAPI
from app.infraestructure.db.base import Base
from app.infraestructure.db.session import engine
from app.api.user_controller import router as user_router


def create_app() -> FastAPI:
    app = FastAPI(title="Backend Take-home")

    # Crear tablas
    Base.metadata.create_all(bind=engine)

    app.include_router(user_router)

    return app

app = create_app()