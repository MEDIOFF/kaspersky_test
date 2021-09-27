from fastapi.middleware.cors import CORSMiddleware

from server.core.app import PublisherApp
from server.utils.on_startup import add_routers


app = PublisherApp()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    await add_routers(app)


