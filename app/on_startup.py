import asyncio
import logging

import pymongo
from pymongo.errors import CollectionInvalid

from services import get_db_connection, get_or_create_exchange, get_or_create_queue, get_rabbit_connection


async def create_collection_if_not_exists():
    db_ = await get_db_connection()
    logging.info("Checking for the existence of a collection")
    try:
        await db_.create_collection("tasks")
        logging.info("Collection created!")
    except CollectionInvalid:
        logging.info("Collection already exists")
        return
    await db_.tasks.create_index([("task_id", pymongo.TEXT)], unique=True, name="task_id_text")


async def create_and_bind_exchange_and_queue_if_not_exists(loop):
    logging.info("Creating and bind exchange and queue")
    rabbit_conn = await get_rabbit_connection(loop)
    channel = await rabbit_conn.channel()
    exchange = await get_or_create_exchange(channel)
    queue = await get_or_create_queue(channel)
    await queue.bind(exchange)
