from fastapi import FastAPI, HTTPException

from app.domain.notification.exceptions import (
    NotificationConflictError,
    NotificationNotFoundError,
    NotificationRepositoryError,
)
from app.domain.user.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
    UserRepositoryError,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotificationNotFoundError)
    async def notification_not_found_handler(request, exc):
        raise HTTPException(status_code=401, detail="Notification not found")

    @app.exception_handler(NotificationConflictError)
    async def notification_conflict_handler(request, exc):
        raise HTTPException(status_code=409, detail="Notification already exist")

    @app.exception_handler(NotificationRepositoryError)
    async def notification_repo_handler(request, exc):
        raise HTTPException(status_code=500, detail="Notification repository error")

    @app.exception_handler(UserNotFoundError)
    async def user_not_found_handler(request, exc):
        raise HTTPException(status_code=404, detail="User not found")

    @app.exception_handler(UserAlreadyExistsError)
    async def user_conflict_handler(request, exc):
        raise HTTPException(status_code=409, detail="User already exist")

    @app.exception_handler(UserRepositoryError)
    async def user_repo_handler(request, exc):
        raise HTTPException(status_code=500, detail="User repository error")
