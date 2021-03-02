from db_functions import Cocktails
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import base64

router = APIRouter(prefix="", tags=["Http Requests"])
cocktailsDB = Cocktails()


@router.get("/getCocktailCover/{cocktailId}")
async def getCocktailCover(cocktailId: int):
    return(str(base64.b64encode(cocktailsDB.readImg(cocktailId)), "utf-8"))
    # return HTMLResponse(html, media_type="image")

# For JSON:
# @router.post("/getCocktailCover")
# async def create_new_game(id: dict):
#     print(id)
#     return id
