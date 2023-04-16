from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from mas.websocket.script.dto.script_response import ScriptResponse
from mas.websocket.websocket_connection_manager import WebsocketConnectionManager

router = APIRouter(tags=["script"])
connection_manage = WebsocketConnectionManager()


@router.websocket("/ws/{meeting_id}")
async def websocket_endpoint(websocket: WebSocket, meeting_id: int):
    await connection_manage.connect(websocket, meeting_id)
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manage.broadcast_script(
                ScriptResponse(name="test", content=data, created_at=datetime.now()),
                meeting_id,
            )
    except WebSocketDisconnect:
        connection_manage.disconnect(websocket, meeting_id)
        await connection_manage.broadcast_text("Client #test left the chat", meeting_id)
