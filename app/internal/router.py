from fastapi import APIRouter
from app.internal.summary import router as summary_router
from app.internal.first_training import router as sixw_router
from app.internal.second_training import router as article_summary_router

router = APIRouter()

router.include_router(summary_router)
router.include_router(sixw_router)
router.include_router(article_summary_router)
