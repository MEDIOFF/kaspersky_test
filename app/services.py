import asyncio
import os

import aio_pika
import motor.motor_asyncio
import pymongo

MONGO_LOGIN = os.getenv("MONGO_LOGIN")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB = os.getenv("MONGO_DB")

RABBIT_LOGIN = os.getenv("RABBIT_LOGIN")
RABBIT_PASS = os.getenv("RABBIT_PASS")
RABBIT_HOST = os.getenv("RABBIT_HOST")


async def get_rabbit_connection(loop_):
    return await aio_pika.connect(
        f"amqp://{RABBIT_LOGIN}:{RABBIT_PASS}@{RABBIT_HOST}/",
        loop=loop_
    )


async def get_db_connection():
    client = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{MONGO_LOGIN}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}")
    return client[MONGO_DB]


async def get_or_create_exchange(channel):
    return await channel.declare_exchange("direct")


async def get_or_create_queue(channel):
    return await channel.declare_queue(os.getenv("QUEUE_NAME"))



