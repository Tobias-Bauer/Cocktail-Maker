from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
from .models.socketManager import WebsocketManager
from db_functions import Cocktails
router = APIRouter(prefix="/ws", tags=["Websocket"])

managers: Dict[str, WebsocketManager] = {}

cocktailsDB = Cocktails()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    if str("mainWs") not in managers.keys():
        managers.update({str("mainWs"): WebsocketManager()})
    await managers[str("mainWs")].connect(websocket)
    manager: WebsocketManager = managers[str("mainWs")]
    await websocket.send_json({"event": "cocktailList", "data": cocktailsDB.readCocktails()})
    try:
        while True:
            try:
                data = await websocket.receive_json()
                print(data['event'])
                if(data['event'] == "submitNewCocktail"):
                    await cocktailsDB.createNewCocktail(data, websocket)
            except Exception as e:
                print(e)
                await websocket.send_json({"event": "msg", "data": "Wrong data"})

    except WebSocketDisconnect:
        manager.disconnect(websocket)
