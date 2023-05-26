from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from mas.websocket.script.dto.script_response import ScriptResponse
from mas.websocket.script.service.script_producing_service import ScriptProducingService
from mas.websocket.websocket_connection_manager import WebsocketConnectionManager

router = APIRouter(tags=["script"])
connection_manage = WebsocketConnectionManager()
script_producing_service = ScriptProducingService()


@router.websocket("/ws/{meeting_id}")
async def websocket_endpoint(websocket: WebSocket, meeting_id: int, user_id: int):
    await connection_manage.connect(websocket, meeting_id)
    try:
        while True:
            data = await websocket.receive_text()
            script_response = ScriptResponse(
                name="test", content=data, created_at=datetime.now()
            )
            await connection_manage.broadcast_script(script_response, meeting_id)
            script_producing_service.consume_script(
                meeting_id, user_id, script_response
            )
    except WebSocketDisconnect:
        connection_manage.disconnect(websocket, meeting_id)
        await connection_manage.broadcast_text("Client #test left the chat", meeting_id)
