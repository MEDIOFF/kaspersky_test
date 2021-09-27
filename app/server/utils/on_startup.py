import asyncio

from publisher import Publisher
from ..routes.core.main import router as MainRouter
from ..routes.api import router as ApiRouter


async def add_routers(app):
    app.include_router(MainRouter)
    app.include_router(ApiRouter)
