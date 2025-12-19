from fastapi import APIRouter
from app.internal.summary import router as summary_router
from app.internal.first_training import router as sixw_router

router = APIRouter()

router.include_router(summary_router)
router.include_router(sixw_router)
