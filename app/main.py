from __future__ import annotations

import logging
import traceback

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.modules.auth.router import router as auth_router
from app.modules.dashboard.router import router as dashboard_router
from app.modules.exams.router import router as exams_router
from app.modules.knowledge_engine.router import router as knowledge_router
from app.modules.smart_study.router import router as smart_study_router
from app.modules.study_guide.router import router as study_guide_router
from app.modules.study_materials.router import router as study_materials_router


logger = logging.getLogger(__name__)


app = FastAPI(
    title="Brain Study API",
    version="1.0.0",
)


# ==========================================================
# GLOBAL ERROR LOGGER
# ==========================================================

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.error(
        "UNHANDLED ERROR:\n%s",
        traceback.format_exc(),
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc),
        },
    )


# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://brain-study.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# API ROUTERS
# ==========================================================

app.include_router(
    auth_router,
    prefix="/api/v1",
)

app.include_router(
    dashboard_router,
    prefix="/api/v1",
)

app.include_router(
    knowledge_router,
    prefix="/api/v1",
)

app.include_router(
    smart_study_router,
    prefix="/api/v1",
)

app.include_router(
    study_materials_router,
    prefix="/api/v1",
)

app.include_router(
    study_guide_router,
    prefix="/api/v1",
)

app.include_router(
    exams_router,
    prefix="/api/v1",
)


# ==========================================================
# ROOT
# ==========================================================

@app.get("/")
def root():
    return {
        "name": "Brain Study API",
        "status": "running",
        "version": "1.0.0",
    }


# ==========================================================
# HEALTH
# ==========================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
    }
