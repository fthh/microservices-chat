from .create_messages_table import run as create_messages_table


async def db_update():
    await create_messages_table()


