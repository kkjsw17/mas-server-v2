from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.responses import HTMLResponse

from mas.script.dto.script_response import ScriptResponse
from mas.script.service.script_websocket_management_service import (
    ScriptWebsocketManagementService,
)

router = APIRouter(tags=["script"])
connection_manage = ScriptWebsocketManagementService()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/3`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get("/web")
async def get_page():
    return HTMLResponse(html)


@router.websocket("/ws/{room_number}")
async def websocket_endpoint(websocket: WebSocket, room_number: int):
    await connection_manage.connect(websocket, room_number)
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manage.broadcast_script(
                ScriptResponse(name="test", content=data, created_at=datetime.now()),
                room_number,
            )
    except WebSocketDisconnect:
        connection_manage.disconnect(websocket, room_number)
        await connection_manage.broadcast_text(
            "Client #test left the chat", room_number
        )
