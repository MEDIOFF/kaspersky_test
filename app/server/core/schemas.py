from typing import Union

from pydantic import BaseModel


class TaskSchema(BaseModel):
    data: Union[str, int]


class ResponseTaskSchema(BaseModel):
    task_id: str
    status: str
    start_time: str
    finish_time: str = None
