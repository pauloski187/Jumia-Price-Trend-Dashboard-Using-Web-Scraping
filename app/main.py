from fastapi import FastAPI
from .routes import router


def get_app() -> FastAPI:
    app = FastAPI(title="Jumia Price Trend API")
    app.include_router(router)
    return app


app = get_app()
