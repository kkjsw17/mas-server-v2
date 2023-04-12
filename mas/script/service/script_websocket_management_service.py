from collections import defaultdict

from fastapi import WebSocket

from mas.script.dto.script_response import ScriptResponse


class ScriptWebsocketManagementService:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = defaultdict(list)

    async def connect(self, websocket: WebSocket, room_number: int):
        await websocket.accept()
        print(self.active_connections)
        self.active_connections[room_number].append(websocket)

    def disconnect(self, websocket: WebSocket, room_number: int):
        self.active_connections[room_number].remove(websocket)

    async def broadcast_text(self, message: str, room_number: int):
        for connection in self.active_connections[room_number]:
            await connection.send_text(message)

    async def broadcast_script(self, script: ScriptResponse, room_number: int):
        for connection in self.active_connections[room_number]:
            await connection.send_text(script.json())
