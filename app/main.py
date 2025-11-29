from fastapi import FastAPI

from app.api.user.user_controller import router as user_router
from app.infraestructure.db.base import Base
from app.infraestructure.db.models.notification_model import NotificationORM
from app.infraestructure.db.models.user_model import UserORM
from app.infraestructure.db.session import engine


def create_app() -> FastAPI:
    app = FastAPI(title="Backend Take-home")

    # Eliminar tablas existentes y recrearlas (solo para desarrollo)
    # En producción, usar migraciones con Alembic
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    app.include_router(user_router)

    return app


app = create_app()
