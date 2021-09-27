import datetime
import logging
import os

import aio_pika

from services import get_or_create_exchange, get_db_connection, get_rabbit_connection


class Publisher:
    db = None
    rabbit_conn = None
    channel = None
    exchange = None

    def __init__(self):
        raise NotImplementedError("Use Server.create(loop) method")

    @classmethod
    async def create(cls, loop):
        self = super().__new__(cls)
        self.db = await get_db_connection()
        self.rabbit_conn = await get_rabbit_connection(loop)
        self.channel = await self.rabbit_conn.channel()
        self.exchange = await get_or_create_exchange(self.channel)
        return self

    async def publish(self, task_id):
        return await self._get_or_create_task(str(task_id))

    async def _get_task_or_none(self, task_id):
        return await self.db.tasks.find_one({"task_id": task_id})

    async def _get_or_create_task(self, task_id):
        task = await self._get_task_or_none(task_id)

        if task is not None:
            logging.info(f"Task '{task_id}' already exists!")
            return task
        data = {
            "task_id": task_id,
            "start_time": datetime.datetime.now().isoformat(),
            "finish_time": None,
            "status": "Waiting"
        }
        await self.db.tasks.insert_one(data)

        await self.exchange.publish(
            aio_pika.Message(
                bytes(task_id, 'utf-8'),
            ),
            os.getenv("QUEUE_ROUTING_KEY")
        )
        logging.info(f"Task '{task_id}' created!")
        return data
