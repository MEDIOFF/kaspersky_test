from fastapi import Depends

from services import get_db_connection


async def get_tasks(db=Depends(get_db_connection)):
    return await db.tasks.find({}).to_list(length=100)
