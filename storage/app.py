import asyncio
import sys
from migrations import *
from DAL.connect import create_db_connect, create_rabbit_connect
from DAL.messages import insert_new_message, deserialize


async def rabbit_consumer(conn, db_conn):
    """Rabbitmq messages handler

    Args:
        conn (aio_pika.Connection): Connection to rabbitmq.
        db_conn (asyncpg.connect): Connection to storage database.

    """
    async with conn:
        queue_name = "event.message.do"
        channel = await conn.channel()
        queue = await channel.declare_queue(
            queue_name,
            auto_delete=True
        )
        async with queue.iterator() as queue_iter:
            async for rabbit_message in queue_iter:
                async with rabbit_message.process():
                    user, text_message = deserialize(rabbit_message.body)
                    await insert_new_message(db_conn, user, text_message)


async def run(loop):
    rabbit_conn = await create_rabbit_connect(loop)
    db_conn = await create_db_connect()

    tasks = [
        asyncio.ensure_future(rabbit_consumer(rabbit_conn, db_conn))
    ]
    await asyncio.wait(tasks)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'migrate':
        migrations_loop = asyncio.get_event_loop()
        migrations_loop.run_until_complete(db_update())
    main()


