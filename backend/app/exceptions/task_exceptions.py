from fastapi import status

from app.exceptions.base import AppException


class TaskNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            message="Task not found",
            status_code=status.HTTP_404_NOT_FOUND
        )