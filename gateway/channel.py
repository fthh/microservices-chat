class Channel:
    """Channel class combines sockets in logical group"""
    _web_sockets = []

    def join(self, socket):
        """Adding new socket in channel"""
        self._web_sockets.append(socket)

    async def broadcast(self, socket, payload: str):
        """Sending payload to all sockets in channel

        Args:
            socket (WebSocketResponse): Initiator.
            payload (str): Payload to send to all channel sockets.
        """
        for ws in self._web_sockets:
            if ws == socket:
                continue
            if ws.closed:
                continue
            await ws.send_str(payload)

    def __init__(self):
        pass
