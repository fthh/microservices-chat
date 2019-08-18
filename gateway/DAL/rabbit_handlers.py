from DAL.messages import serialize_message, deserialize_message


async def rabbit_consumer_messages_ok(conn):
    """Rabbitmq messages success handler

    Args:
        conn (aio_pika.Connection): Connection to rabbitmq.

    """
    async with conn:
        queue_name = "event.message.ok"
        channel = await conn.channel()
        queue = await channel.declare_queue(
            queue_name,
            auto_delete=True
        )
        async with queue.iterator() as queue_iter:
            async for rabbit_message in queue_iter:
                async with rabbit_message.process():
                    message_id, user, text_message = deserialize_message(rabbit_message.body)
                    print("[+] Message: {} {} {}".format(message_id, user, text_message))


async def rabbit_consumer_messages_ko(conn):
    """Rabbitmq messages errors handler

    Args:
        conn (aio_pika.Connection): Connection to rabbitmq.

    """
    async with conn:
        queue_name = "event.message.ko"
        channel = await conn.channel()
        queue = await channel.declare_queue(
            queue_name,
            auto_delete=True
        )
        async with queue.iterator() as queue_iter:
            async for rabbit_message in queue_iter:
                async with rabbit_message.process():
                    message_id, user, text_message = deserialize_message(rabbit_message.body)
                    print("[-] Message: {} {} {}".format(message_id, user, text_message))
