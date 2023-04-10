import inject
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from mas.script.service.script_websocket_management_service import (
    ScriptWebsocketManagementService,
)

router = APIRouter(tags=["script"])
connection_manage = inject.instance(ScriptWebsocketManagementService)


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await connection_manage.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manage.send_message(f"You wrote: {data}", websocket)
            await connection_manage.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        connection_manage.disconnect(websocket)
        await connection_manage.broadcast(f"Client #{client_id} left the chat")
