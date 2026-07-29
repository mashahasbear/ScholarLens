from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage application startup and shutdown."""

    print(f"Starting {settings.app_name} v{settings.app_version}")
    yield
    print(f"Stopping {settings.app_name}")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "A deterministic academic literature-review automation platform "
        "with paper discovery, metadata analysis, citation networks, "
        "structured extraction and evidence-based gap indicators."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    api_router,
    prefix=settings.api_prefix,
)


@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    """Return basic application information."""

    return {
        "message": "Welcome to ScholarLens",
        "documentation": "/docs",
        "health": f"{settings.api_prefix}/health",
    }