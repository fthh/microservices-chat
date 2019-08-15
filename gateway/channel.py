class Channel:
    
    _web_sockets = []

    def join(self, socket):
        self._web_sockets.append(socket)

    async def broadcast(self, socket, payload: str):
        for ws in self._web_sockets:
            if ws == socket:
                continue
            await ws.send_str(payload)

    def __init__(self):
        pass
