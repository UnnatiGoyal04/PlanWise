import uuid

from fastapi import FastAPI, Request


def register_request_id_middleware(app: FastAPI):

    @app.middleware("http")
    async def add_request_id(request: Request, call_next):
        request.state.request_id = str(uuid.uuid4())

        response = await call_next(request)

        response.headers["X-Request-ID"] = request.state.request_id

        return response