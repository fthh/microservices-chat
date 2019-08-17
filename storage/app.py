import asyncio
import sys
from migrations import *
from DAL.connect import create_db_connect, create_rabbit_connect
from DAL.messages import insert_new_message
import DAL.proto.protoc_out.message_pb2 as proto


def deserialize(raw_data):
    message = proto.Message()
    message.ParseFromString(raw_data)
    return message.user, message.message


async def rabbit_consumer(conn, db_conn):
    async with conn:
        queue_name = "inserting_messages_queue"
        channel = await conn.channel()
        queue = await channel.declare_queue(
            queue_name,
            auto_delete=True
        )
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    user, message = deserialize(message.body)
                    await insert_new_message(db_conn, user, message)


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


