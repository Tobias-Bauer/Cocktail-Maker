import sqlite3
import requests


class Cocktails():
    def __init__(self) -> None:
        self.connection = sqlite3.connect('database.db')
        self.sql_create_cocktail_table = """ CREATE TABLE IF NOT EXISTS cocktails (
                                            id integer PRIMARY KEY,
                                            title text NOT NULL,
                                            description text,
                                            img text
                                        ); """
        self.create_table(self.sql_create_cocktail_table)

    def create_table(self, create_table_sql):
        try:
            c = self.connection.cursor()
            c.execute(create_table_sql)
        except Exception as e:
            print(e)

    async def createNewCocktail(self, data, websocket):
        response = None
        try:
            response = requests.get(data["img"])
        except:
            await websocket.send_json({"event": "msg", "data": "Image url is invalid!"})
            return
        if response.ok:
            sql = 'INSERT INTO cocktails VALUES (?,?,?,?)'.format(
                self.sql_create_cocktail_table)
            self.connection.execute(
                sql, (None, data["title"], data["description"], sqlite3.Binary(response.content)))
            self.connection.commit()
            print("Created new Cocktail")
        else:
            await websocket.send_json({"event": "msg", "data": "Image url is invalid!"})

    def readCocktails(self):
        sql = 'SELECT * FROM {}'.format('cocktails')
        cursor = self.connection.execute(sql)
        data = []
        for row in cursor:
            data.append({
                "id": row[0],
                "title": row[1],
                "description": row[2]
            })
        return data

    def readImg(self, cocktailId):
        sql = 'SELECT img FROM cocktails WHERE id = {}'.format(cocktailId)
        data = self.connection.execute(sql).fetchone()

        return data[0]
