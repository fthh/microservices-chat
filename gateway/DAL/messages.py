import aio_pika
from .connect import create_rabbit_connect
import DAL.proto.protoc_out.message_pb2 as proto
import random


def serialize_message(message_id: int, user: str, text: str) -> str:
    """Serializing user's message to proto string

    Args:
        message_id (int): Message identifier in rabbitmq.
        user (str): Username.
        text (str): Text message.
    """
    message = proto.Message()
    message.id = message_id
    message.user = user
    message.message = text
    return message.SerializeToString()


def deserialize_message(raw_data):
    """Deserializing proto bytes from rabbitmq to message object

    Args:
        raw_data (str): Raw data for deserializing.
    """
    message = proto.Message()
    message.ParseFromString(raw_data)
    return message.id, message.user, message.message


async def publish_new_message(user: str, message: str):
    rabbit_connect = await create_rabbit_connect()

    routing_key = "event.message.do"

    channel = await rabbit_connect.channel()

    msg = serialize_message(random.randint(1, 10000), user, message)

    await channel.default_exchange.publish(
        aio_pika.Message(
            body=msg
        ),
        routing_key=routing_key
    )

    await rabbit_connect.close()
