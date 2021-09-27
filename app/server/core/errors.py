from pydantic import BaseModel


class InvalidTaskData(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            'example': {'detail': "data can't be empty"}
        }
