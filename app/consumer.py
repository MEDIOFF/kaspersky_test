import asyncio
import datetime
import logging
import random

import aio_pika

from services import get_or_create_queue, get_db_connection, get_rabbit_connection


class Consumer:
    db = None
    conn = None

    def __init__(self):
        raise NotImplementedError("Use Worker.create(loop) method")

    @classmethod
    async def create(cls, loop):
        self = super().__new__(cls)
        self.db = await get_db_connection()
        self.conn = await get_rabbit_connection(loop)
        return self

    async def _process_message(self, message: aio_pika.IncomingMessage):
        await asyncio.sleep(random.randint(1, 10))
        async with message.process():
            data = message.body.decode()
            logging.info(f"Task {data} is done")
            await self.db.tasks.update_one({"task_id": data},
                                           {"$set": {
                                               "finish_time": datetime.datetime.now().isoformat(),
                                               "status": "Done"
                                           }})

    async def run(self):
        channel = await self.conn.channel()

        queue = await get_or_create_queue(channel)
        await queue.consume(self._process_message)
