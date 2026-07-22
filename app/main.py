from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.modules.auth.router import router as auth_router
from app.modules.knowledge_engine.router import router as knowledge_router
from app.modules.smart_study.router import router as smart_study_router
from app.modules.study_materials.router import router as study_materials_router
from app.modules.study_guide.router import router as study_guide_router
from app.modules.exams.router import router as exams_router


app = FastAPI(
    title="Brain Study API",
    version="1.0.0",
)


# CORS configuration
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


app.include_router(auth_router, prefix="/api/v1")
app.include_router(knowledge_router, prefix="/api/v1")
app.include_router(smart_study_router, prefix="/api/v1")
app.include_router(study_materials_router, prefix="/api/v1")
app.include_router(study_guide_router, prefix="/api/v1")
app.include_router(exams_router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "name": "Brain Study API",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }
