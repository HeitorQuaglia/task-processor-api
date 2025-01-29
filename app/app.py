from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import process_data


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["POST", "GET", "OPTIONS"],
        allow_headers=["*"],
    )

    app.include_router(process_data.router)

    return app
