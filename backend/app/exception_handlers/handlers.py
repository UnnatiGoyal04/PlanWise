from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.base import AppException
from app.logging.logger import logger

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request,
        exc: AppException
    ):
        logger.exception(
            f"Unhandled exception on {request.method} {request.url.path}"
        )
        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal server error"
            }
        )