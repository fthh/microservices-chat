import aio_pika
from .connect import create_rabbit_connect


async def publish_new_message(user, message):
    rabbit_connect = await create_rabbit_connect()

    routing_key = "inserting_messages_queue"

    channel = await rabbit_connect.channel()

    await channel.default_exchange.publish(
        aio_pika.Message(
            body='Hello {}'.format(routing_key).encode()
        ),
        routing_key=routing_key
    )

    await rabbit_connect.close()
