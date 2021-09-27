import asyncio

from fastapi import FastAPI

from publisher import Publisher


class PublisherApp(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        loop = asyncio.get_event_loop()
        self.publisher = loop.run_until_complete(Publisher.create(loop))