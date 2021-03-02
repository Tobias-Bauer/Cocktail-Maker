from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import websockets, http
import uvicorn

app = FastAPI()
app.include_router(websockets.router)
app.include_router(http.router)

app.add_middleware(CORSMiddleware, allow_origins=['*'],
                   allow_methods=["*"], allow_headers=["*"])

uvicorn.run(app, port=10000, host='0.0.0.0')
# class SocketFunctions(WebSocketServerProtocol):

#     def onConnect(self, request):
#         print("Client connecting: {0}".format(request.peer))
#         self.connection = db
#         create_table(self, sql_create_cocktail_table)

#     def onOpen(self):
#         self.sendMessage(json.dumps({"event": "cocktailList", "data": readCocktails(
#             self)}).encode('utf-8'))
#         #response = requests.get("https://api.cocktails.de/sites/default/files/styles/is_detail/public/2020-02/Wodka_Recipe-04_Sex-on-the-beach-min.jpg")
#         # print(base64.b64encode(response))

#     def onMessage(self, payload, isBinary):
#         if isBinary:
#             print("Binary message received: {0} bytes".format(len(payload)))
#         else:
#             try:
#                 data = json.loads(payload)
#                 if(data["event"] == "submitNewCocktail"):
#                     createNewCocktail(self, data)
#             except Exception as e:
#                 print(e)

#         # echo back message verbatim
#         self.sendMessage(payload, isBinary)

#     def onClose(self, wasClean, code, reason):
#         print("WebSocket connection closed: {0}".format(reason))


# factory = WebSocketServerFactory("ws://127.0.0.1:9000")
# factory.protocol = SocketFunctions
# loop = asyncio.get_event_loop()
# coro = loop.create_server(factory, '0.0.0.0', 9000)
# server = loop.run_until_complete(coro)
# try:
#     loop.run_forever()
# except KeyboardInterrupt:
#     pass
# finally:
#     server.close()
#     loop.close()
