from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
from models.socketManager import WebsocketManager
from db_main import Database
from general_functions import General
router = APIRouter(prefix="/ws", tags=["Websocket"])

managers: Dict[str, WebsocketManager] = {}

db = Database()
cocktailsDB = db.getCocktailDb()
ingredientsDB = db.getIngredientsDb()
general = General()


async def sendCocktailList(websocket):
    await websocket.send_json({"event": "cocktailList", "data": general.hijackCocktailData(cocktailsDB.readCocktails())})


async def broadcastCocktailData(manager):
    await manager.broadcast({"event": "cocktailList", "data": general.hijackCocktailData(cocktailsDB.readCocktails())})


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    if str("mainWs") not in managers.keys():
        managers.update({str("mainWs"): WebsocketManager()})
    await managers[str("mainWs")].connect(websocket)
    manager: WebsocketManager = managers[str("mainWs")]
    # Send Cocktail and Ingredient Lists
    await sendCocktailList(websocket)
    await websocket.send_json({"event": "ingredientList", "data": ingredientsDB.readIngredients()})
    try:
        while True:
            data = await websocket.receive_json()
            print(data['event'])
            if(data['event'] == "submitNewCocktail"):
                if(data['ingredients'][0]):
                    await cocktailsDB.createNewCocktail(data, websocket, manager, broadcastCocktailData)
            if(data['event'] == "changeImg"):
                await cocktailsDB.updateImg(data, websocket, manager, broadcastCocktailData)
            if(data['event'] == "changeText"):
                await cocktailsDB.updateTexts(data)
                await broadcastCocktailData(manager)
            if(data['event'] == "removeCocktail"):
                cocktailsDB.removeCocktail(data["id"])
                await broadcastCocktailData(manager)
            if(data['event'] == "submitNewIngredient"):
                ingredientsDB.createIngredient(data)
                await manager.broadcast({"event": "ingredientList", "data": ingredientsDB.readIngredients()})
            if(data['event'] == "setPump"):
                ingredientsDB.setPump(data)
                await broadcastCocktailData(manager)
                await manager.broadcast({"event": "ingredientList", "data": ingredientsDB.readIngredients()})
            if(data['event'] == "removePump"):
                ingredientsDB.removePump(data["pump"])
                await broadcastCocktailData(manager)
                await manager.broadcast({"event": "ingredientList", "data": ingredientsDB.readIngredients()})
            if(data["event"] == "updateCocktailIngredients"):
                await cocktailsDB.updateIngredients(data, websocket)
                await broadcastCocktailData(manager)
            if(data["event"] == "favorite"):
                cocktailsDB.favorite(data["id"])
                await broadcastCocktailData(manager)
            if(data["event"] == "unfavorite"):
                cocktailsDB.unfavorite(data["id"])
                await broadcastCocktailData(manager)

    except WebSocketDisconnect as e:
        print("Disconnecting a client...")
        print(e)
        # await websocket.send_json({"event": "msg", "data": "Wrong data/Error: {}".format(e)})
        manager.disconnect(websocket)
