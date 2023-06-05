from collections import defaultdict

from chat.dto.script_dto import ScriptDto
from fastapi import WebSocket


class WebsocketConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = defaultdict(list)

    async def connect(self, websocket: WebSocket, meeting_id: int):
        await websocket.accept()
        self.active_connections[meeting_id].append(websocket)

    def disconnect(self, websocket: WebSocket, meeting_id: int):
        self.active_connections[meeting_id].remove(websocket)

    async def broadcast_text(self, message: str, meeting_id: int):
        for connection in self.active_connections[meeting_id]:
            await connection.send_text(message)

    async def broadcast_script(self, script_dto: ScriptDto, meeting_id: int):
        for connection in self.active_connections[meeting_id]:
            await connection.send_text(script_dto.json(ensure_ascii=False))
