
class Ingredients(object):
    def __init__(self, arg) -> None:
        self.connection = arg

    def createIngredient(self, data):
        sql = 'INSERT INTO ingredients VALUES (?,?,?)'
        self.connection.execute(
            sql, (None, data["ingredient"], None))
        self.connection.commit()
        print("Created new Ingredient: {0}".format(data["ingredient"]))

    def setPump(self, data):
        self.removePump(data["pump"])
        sql = 'UPDATE ingredients SET pump = ? WHERE ingredient = ?'
        self.connection.execute(
            sql, (data["pump"], data["ingredient"]))
        self.connection.commit()

    def removePump(self, pump):
        sql = 'UPDATE ingredients SET pump = ? WHERE pump = ?'
        self.connection.execute(
            sql, (None, pump))
        self.connection.commit()

    def readIngredients(self):
        sql = 'SELECT * FROM ingredients'
        cursor = self.connection.execute(sql)
        data = []
        for row in cursor:
            data.append({
                "id": row[0],
                "ingredient": row[1],
                "pump": row[2]
            })
        return data

    def getMotorList(self):
        # Return List with current used motors and their current ingredient
        sql = 'SELECT * FROM ingredients'
        cursor = self.connection.execute(sql)
        data = []
        for row in cursor:
            if(row[2]):
                data.append({
                    "ingredient": row[1],
                    "pump": row[2]
                })
        return data
        pass
