from db_main import Database
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import base64

router = APIRouter(prefix="", tags=["Http Requests"])
db = Database()
cocktailsDB = db.getCocktailDb()


@router.get("/getCocktailCover/{cocktailId}")
async def getCocktailCover(cocktailId: int):
    img = cocktailsDB.readImg(cocktailId)
    if(img != None):
        return(str(base64.b64encode(img), "utf-8"))
    # return HTMLResponse(html, media_type="image")

# For JSON:
# @router.post("/getCocktailCover")
# async def create_new_game(id: dict):
#     print(id)
#     return id
