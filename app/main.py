from __future__ import annotations

from fastapi import FastAPI

from app.modules.auth.router import router as auth_router
from app.modules.exams.router import router as exams_router
from app.modules.knowledge_engine.router import router as knowledge_router
from app.modules.study_guide.router import router as study_guide_router

app = FastAPI(
    title="Brain Study API",
    version="1.0.0",
)

API_PREFIX = "/api/v1"

app.include_router(
    auth_router,
    prefix=API_PREFIX,
)

app.include_router(
    knowledge_router,
    prefix=API_PREFIX,
)

app.include_router(
    study_guide_router,
    prefix=API_PREFIX,
)

app.include_router(
    exams_router,
    prefix=API_PREFIX,
)


@app.get("/")
def root():
    return {
        "application": "Brain Study",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }
