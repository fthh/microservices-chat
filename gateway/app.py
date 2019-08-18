import asyncio
import os
import json
import aiohttp.web
from channel import Channel
from DAL.connect import create_rabbit_connect_loop
from DAL.messages import publish_new_message
from DAL.rabbit_handlers import rabbit_consumer_messages_ok, rabbit_consumer_messages_ko

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8001))

channel = Channel()


async def websocket_handler(request):
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)

    channel.join(ws)
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            data = json.loads(msg.data)
            try:
                await publish_new_message(data['user'], data['text'])
            except ConnectionError:
                pass
            await channel.broadcast(ws, msg.data)

    return ws


async def static_handler(request):
    return aiohttp.web.HTTPFound('/index.html')


async def run_rabbit_handlers(loop):
    while True:
        try:
            rabbit_connection = await create_rabbit_connect_loop(loop)
        except ConnectionError:
            await asyncio.sleep(1)
        else:
            break
    tasks = [
        asyncio.ensure_future(rabbit_consumer_messages_ok(rabbit_connection)),
        asyncio.ensure_future(rabbit_consumer_messages_ko(rabbit_connection)),
    ]
    await asyncio.wait(tasks)


async def run_server(app):
    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner, HOST, PORT)
    print("======= Serving on http://{}:{}/ ======".format(HOST, PORT))
    await site.start()
    await asyncio.sleep(8640000)  # 100 days
    await runner.cleanup()


def main():
    loop = asyncio.get_event_loop()
    app = aiohttp.web.Application(loop=loop)

    app.router.add_route('GET', '/ws', websocket_handler)

    app.router.add_route('GET', '/', static_handler)
    app.router.add_static('/static', './www/static')
    app.router.add_static('/', './www/')

    tasks = [
        loop.create_task(run_rabbit_handlers(loop)),
        loop.create_task(run_server(app)),
    ]
    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    main()
