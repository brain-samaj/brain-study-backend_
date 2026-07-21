from fastapi import APIRouter

from app.modules.auth.router import router as auth_router
from app.modules.study_materials.router import router as study_materials_router

api_router = APIRouter(
    prefix="/api/v1",
)

api_router.include_router(auth_router)
api_router.include_router(study_materials_router)
