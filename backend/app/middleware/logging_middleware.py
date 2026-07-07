from fastapi import FastAPI, Request
import time

from app.logging.logger import logger

def register_logging_middleware(app: FastAPI):

    @app.middleware("http")
    async def log_requests(request: Request, call_next):

        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = (time.perf_counter() - start_time) * 1000
        logger.info(
            f"{request.method} "
            f"{request.url.path} | "
            f"{response.status_code} | "
            f"{process_time:.2f} ms"
        )

        return response