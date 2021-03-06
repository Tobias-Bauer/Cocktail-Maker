import sqlite3
import requests
from functools import reduce
import json


class Cocktails(object):
    def __init__(self, arg) -> None:
        self.connection = arg

    async def createNewCocktail(self, data, websocket, manager, func):
        # check if ingredient list is correct
        if(await self.checkIngredientList(data['ingredients'], websocket)):
            response = None
            if(data["img"] == ""):
                sql = 'INSERT INTO cocktails VALUES (?,?,?,?,?,?)'
                self.connection.execute(
                    sql, (None, data["title"], data["description"], None, json.dumps(data['ingredients']), False))
                self.connection.commit()
                print("Created new Cocktail: {0}".format(data["title"]))
                await func(manager)
                return
            try:
                response = requests.get(data["img"])
            except:
                await websocket.send_json({"event": "msg", "data": "Image url is invalid!"})
                return
            if response.ok:
                sql = 'INSERT INTO cocktails VALUES (?,?,?,?,?)'
                self.connection.execute(
                    sql, (None, data["title"], data["description"], sqlite3.Binary(response.content), json.dumps(data['ingredients'])))
                self.connection.commit()
                print("Created new Cocktail: {0}".format(data["title"]))
                await func(manager)
            else:
                await websocket.send_json({"event": "msg", "data": "Image url is invalid!"})

    async def updateImg(self, data, websocket, manager, func):
        response = None
        try:
            response = requests.get(data["img"])
        except:
            await websocket.send_json({"event": "msg", "data": "Image url is invalid!"})
            return
        if response.ok:
            sql = 'UPDATE cocktails SET img = ? WHERE id = ?'
            self.connection.execute(
                sql, (sqlite3.Binary(response.content), data["id"]))
            self.connection.commit()
            print("Updated a Cocktail Image")
            await func(manager)
        else:
            await websocket.send_json({"event": "msg", "data": "Image url is invalid!"})

    def updateTexts(self, data):
        sql = 'UPDATE cocktails SET title = ?, description = ? WHERE id = ?'
        self.connection.execute(
            sql, (data["title"], data["description"], data["id"]))
        self.connection.commit()

    async def updateIngredients(self, data, websocket):
        if(await self.checkIngredientList(data["ingredients"], websocket)):
            sql = 'UPDATE cocktails SET ingredients = ? WHERE id = ?'
            self.connection.execute(
                sql, (json.dumps(data["ingredients"]), data["id"]))
            self.connection.commit()

    def favorite(self, cocktailId):
        sql = 'UPDATE cocktails SET favorite = ? WHERE id = ?'
        self.connection.execute(
            sql, (True, cocktailId))
        self.connection.commit()

    def unfavorite(self, cocktailId):
        sql = 'UPDATE cocktails SET favorite = ? WHERE id = ?'
        self.connection.execute(
            sql, (False, cocktailId))
        self.connection.commit()

    def readCocktails(self):
        sql = 'SELECT * FROM cocktails'
        cursor = self.connection.execute(sql)
        data = []
        for row in cursor:
            data.append({
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "ingredients": json.loads(row[4]),
                "favorite": row[5]
            })
        return data

    def readImg(self, cocktailId):
        sql = 'SELECT img FROM cocktails WHERE id = {}'.format(cocktailId)
        data = self.connection.execute(sql).fetchone()
        return data[0]

    def removeCocktail(self, id):
        sql = 'DELETE FROM cocktails WHERE id=?'
        cur = self.connection.cursor()
        cur.execute(sql, (id,))
        self.connection.commit()

    def getIngredientList(self, cocktailId):
        # Return Ingredients of one Cocktail
        sql = 'SELECT ingredients FROM cocktails WHERE id = {}'.format(
            cocktailId)
        data = json.loads(self.connection.execute(sql).fetchone()[0])
        arr = []
        for el in data:
            arr.append(el["ingredient"])
        return arr

    async def checkIngredientList(self, list, websocket) -> bool:
        # Check if round sums up to 100
        arr = []
        for record in list:
            arr.append(record['value'])
        if round(reduce((lambda x, y: x + y), arr)) != 100:
            await websocket.send_json({"event": "msg", "data": "Not 100%!"})
            return False
        # Check for no doubled ingredients
        seen = set()
        for record in list:
            ingredient = record['ingredient']
            if ingredient in seen:
                await websocket.send_json({"event": "msg", "data": "Duplicate Ingredients!"})
                return False
            seen.add(ingredient)
        del seen
        # Check for null values
        for record in list:
            if record['ingredient'] == None:
                await websocket.send_json({"event": "msg", "data": "Empty Ingredient!"})
                return False
        return True
