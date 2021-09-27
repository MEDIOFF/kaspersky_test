import asyncio
import logging

from hypercorn import Config
from hypercorn.asyncio import serve

from server.main import app
from on_startup import create_collection_if_not_exists, create_and_bind_exchange_and_queue_if_not_exists
from consumer import Consumer


config = Config()
config.bind = ["0.0.0.0:8080"]

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s | %(levelname)-8s | %(lineno)04d | %(message)s')
    loop = asyncio.get_event_loop()

    loop.run_until_complete(create_collection_if_not_exists())
    loop.run_until_complete(create_and_bind_exchange_and_queue_if_not_exists(loop))

    consumer = loop.run_until_complete(Consumer.create(loop))

    loop.create_task(consumer.run())

    loop.create_task(serve(app, config))

    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(consumer.conn.close())
