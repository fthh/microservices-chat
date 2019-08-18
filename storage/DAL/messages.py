import asyncpg
from .proto.protoc_out import message_pb2 as proto
import aio_pika


async def alert_error_message(conn: aio_pika.Connection, message_id: int, user: str, message: str):
    routing_key = "event.message.ko"
    channel = await conn.channel()
    msg = serialize_message(message_id, user, message)
    await channel.default_exchange.publish(
        aio_pika.Message(
            body=msg
        ),
        routing_key=routing_key
    )


async def alert_success_message(conn: aio_pika.Connection, message_id: int, user: str, message: str):
    routing_key = "event.message.ok"
    channel = await conn.channel()
    msg = serialize_message(message_id, user, message)
    await channel.default_exchange.publish(
        aio_pika.Message(
            body=msg
        ),
        routing_key=routing_key
    )


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


def deserialize(raw_data):
    """Deserializing proto bytes from rabbitmq to message object

    Args:
        raw_data (str): Raw data for deserializing.
    """
    message = proto.Message()
    message.ParseFromString(raw_data)
    return message.id, message.user, message.message


async def insert_new_message(conn: asyncpg.connect, message_id: int, user: str, message: str):
    await conn.fetch('''
        INSERT INTO messages (user_name, message_text) 
        VALUES ($1, $2)''',
        user, message)
