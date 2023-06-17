import os
from datetime import datetime

from chat.dto.script_dto import ScriptDto
from chat.service.script_producing_service import ScriptProducingService
from chat.utils.config import Config
from chat.websocket_connection_manager import WebsocketConnectionManager
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.responses import HTMLResponse

router = APIRouter(tags=["Script"])

connection_manager = WebsocketConnectionManager()
script_producing_service = ScriptProducingService(Config(os.getenv("PHASE", "local")))


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
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
            var ws = new WebSocket(encodeURI(`ws://localhost:8000/ws/3?user_id=${client_id}&user_name=${"강아지"}`));
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


@router.websocket("/ws/{meeting_id}")
async def websocket_endpoint(
    websocket: WebSocket, meeting_id: int, user_id: int, user_name: str
):
    await connection_manager.connect(websocket, meeting_id)
    try:
        while True:
            content = await websocket.receive_text()
            script_dto = ScriptDto(
                name=user_name, content=content, created_at=datetime.now()
            )
            await connection_manager.broadcast_script(script_dto, meeting_id)
            script_producing_service.produce_script(meeting_id, user_id, script_dto)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket, meeting_id)
        await connection_manager.broadcast_text(
            "Client #test left the chat", meeting_id
        )
