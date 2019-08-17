import aio_pika


async def create_rabbit_connect():
    conn = await aio_pika.connect_robust(
        "amqp://guest:guest@rabbit/"
    )
    return conn

