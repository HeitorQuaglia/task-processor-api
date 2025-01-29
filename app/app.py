from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import data_router

def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Permite acesso de qualquer origem (ajuste conforme necessidade)
        allow_credentials=True,
        allow_methods=["POST", "GET", "OPTIONS"],
        allow_headers=["*"],
    )

    app.include_router(data_router.router)

    return app
