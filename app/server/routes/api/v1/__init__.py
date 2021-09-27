from fastapi import APIRouter
from .task import router as TaskRouter

router = APIRouter(prefix='/v1')

router.include_router(TaskRouter, tags=["Task API"])