from fastapi import APIRouter, HTTPException
from fastapi.requests import Request

from server.core.errors import InvalidTaskData
from server.core.schemas import ResponseTaskSchema, TaskSchema

router = APIRouter()


@router.post("/createTask", response_model=ResponseTaskSchema,
             responses={400: {"model": InvalidTaskData,
                              "description": "Invalid task data"}})
async def create_task(task: TaskSchema, request: Request):
    publisher = request.app.publisher
    if isinstance(task.data, str) and len(task.data) < 1:
        raise HTTPException(status_code=400, detail="Invalid task data")
    res = await publisher.publish(task.data)
    if "_id" in res.keys():
        res.pop("_id")
    return res
