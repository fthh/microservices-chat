import asyncio
import os
import json
import aiohttp.web
from channel import Channel
from DAL.messages import publish_new_message

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
            await publish_new_message(data['user'], data['text'])
            await channel.broadcast(ws, msg.data)

    return ws


async def static_handler(request):
    return aiohttp.web.HTTPFound('/index.html')


def main():
    loop = asyncio.get_event_loop()
    app = aiohttp.web.Application(loop=loop)
    
    app.router.add_route('GET', '/ws', websocket_handler)

    app.router.add_route('GET', '/', static_handler)
    app.router.add_static('/static', './www/static')
    app.router.add_static('/', './www/')

    aiohttp.web.run_app(app, host=HOST, port=PORT)


if __name__ == '__main__':
    main()
