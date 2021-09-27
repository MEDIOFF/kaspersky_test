from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from server.dependencies import get_tasks
from server.utils.helpers import templates

router = APIRouter(include_in_schema=False)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, tasks=Depends(get_tasks)):
    return templates.TemplateResponse('index.html', {'request': request, "tasks": tasks})
