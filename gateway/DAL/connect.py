import aio_pika

RABBIT_URL = "amqp://guest:guest@rabbit/"


async def create_rabbit_connect():
    conn = await aio_pika.connect_robust(
        RABBIT_URL,
    )
    return conn


async def create_rabbit_connect_loop(loop):
    conn = await aio_pika.connect_robust(
        RABBIT_URL, loop=loop
    )
    return conn

