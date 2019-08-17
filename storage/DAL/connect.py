import os
import asyncpg
import aio_pika

DB_PASSWORD = os.getenv('DB_PASSWORD', '123')
DB_NAME = os.getenv('DB_NAME', 'chat_storage')
DB_HOST = os.getenv('DB_HOST', 'storage_db')
DB_USER = os.getenv('DB_USER', 'postgres')


async def create_db_connect() -> asyncpg.connect:
    conn = await asyncpg.connect(user=DB_USER, password=DB_PASSWORD,
                                 database=DB_NAME, host=DB_HOST)
    return conn


async def create_rabbit_connect(loop):
    conn = await aio_pika.connect_robust(
        "amqp://guest:guest@rabbit/", loop=loop
    )
    return conn

