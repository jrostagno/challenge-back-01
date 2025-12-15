from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.auth.auth_controller import router as auth_router
from app.api.exception_handlers import register_exception_handlers
from app.api.notification.notification_controller import router as notification_router
from app.api.user.user_controller import router as user_router
from app.infraestructure.db.base import Base
from app.infraestructure.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔹 Startup
    Base.metadata.create_all(bind=engine)
    yield
    # 🔹 Shutdown (no hacemos nada ahora)


def create_app() -> FastAPI:
    app = FastAPI(title="Backend Take-home", lifespan=lifespan)

    app.include_router(notification_router)
    app.include_router(user_router)
    app.include_router(auth_router)

    register_exception_handlers(app)

    return app


app = create_app()
