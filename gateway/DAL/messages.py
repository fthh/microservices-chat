import aio_pika
from .connect import create_rabbit_connect
import DAL.proto.protoc_out.message_pb2 as proto


def serialize_message(user: str, text: str) -> str:
    """Serializing user's message to proto string

    Args:
        user (str): Username.
        text (str): Text message.
    """
    message = proto.Message()
    message.user = user
    message.message = text
    return message.SerializeToString()


async def publish_new_message(user: str, message: str):
    rabbit_connect = await create_rabbit_connect()

    routing_key = "event.message.do"

    channel = await rabbit_connect.channel()

    msg = serialize_message(user, message)

    await channel.default_exchange.publish(
        aio_pika.Message(
            body=msg
        ),
        routing_key=routing_key
    )

    await rabbit_connect.close()
