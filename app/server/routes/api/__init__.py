from fastapi import APIRouter
from .v1 import router as ApiV1Router

router = APIRouter(prefix='/api')

router.include_router(ApiV1Router)