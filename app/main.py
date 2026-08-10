"""FastAPI application factory for U.Perfect Social Commerce OS."""

from __future__ import annotations

from fastapi import FastAPI

from app.config import Settings
from app.database import Database


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create a locally runnable API without exposing runtime secrets."""

    app = FastAPI(title="U.Perfect Social Commerce OS")
    app.state.settings = settings or Settings.from_environment()
    app.state.db = Database(app.state.settings.database_path)

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "brand": "U.Perfect"}

    return app


app = create_app()
