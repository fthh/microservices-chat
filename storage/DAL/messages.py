import asyncpg
from .proto.protoc_out import message_pb2 as proto


def deserialize(raw_data):
    """Deserializing proto bytes from rabbitmq to message object

    Args:
        raw_data (str): Raw data for deserializing.
    """
    message = proto.Message()
    message.ParseFromString(raw_data)
    return message.user, message.message


async def insert_new_message(conn: asyncpg.connect, user: str, message: str):
    await conn.fetch('''
        INSERT INTO messages (user_name, message_text) 
        VALUES ($1, $2)''',
        user, message)
