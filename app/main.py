from fastapi import FastAPI
from .routes import router
from .scheduler import start_scheduler, shutdown_scheduler


def get_app() -> FastAPI:
    app = FastAPI(title="Jumia Price Trend API")
    app.include_router(router)

    @app.on_event("startup")
    def _startup():
        start_scheduler(app)

    @app.on_event("shutdown")
    def _shutdown():
        shutdown_scheduler(app)
    return app


app = get_app()
