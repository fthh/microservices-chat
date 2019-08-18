import asyncio
import asyncpg
import os

DB_PASSWORD = os.getenv('DB_PASSWORD', '123')
DB_NAME = os.getenv('DB_NAME', 'chat_storage')
DB_HOST = os.getenv('DB_HOST', 'storage_db')
DB_USER = os.getenv('DB_USER', 'postgres')


async def run():
    conn = await asyncpg.connect(user=DB_USER, password=DB_PASSWORD,
                                 database=DB_NAME, host=DB_HOST)
    await conn.fetch('''
        CREATE TABLE IF NOT EXISTS messages (
            user_name VARCHAR (45) NOT NULL,
            message_text VARCHAR (500) NOT NULL
        );
    ''')
    await conn.close()

