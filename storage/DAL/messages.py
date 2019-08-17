import asyncpg


async def insert_new_message(conn: asyncpg.connect, user: str, message: str):
    # TODO
    values = await conn.fetch('''SELECT * FROM messages''')
    print(values)
