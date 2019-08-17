import asyncpg


async def insert_new_message(conn: asyncpg.connect, user: str, message: str):
    await conn.fetch('''
        INSERT INTO messages (user_name, message_text) 
        VALUES ($1, $2)''',
        user, message)
