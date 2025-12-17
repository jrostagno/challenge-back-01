from fastapi import FastAPI

from app.api.auth.auth_controller import router as auth_router
from app.api.exception_handlers import register_exception_handlers
from app.api.notification.notification_controller import router as notification_router
from app.api.user.user_controller import router as user_router


def create_app() -> FastAPI:
    app = FastAPI(title="Backend Take-home")

    app.include_router(notification_router)
    app.include_router(user_router)
    app.include_router(auth_router)

    register_exception_handlers(app)

    return app


app = create_app()
