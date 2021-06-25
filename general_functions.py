from db_main import Database

db = Database()
cocktailsDB = db.getCocktailDb()
ingredientsDB = db.getIngredientsDb()


class General():

    def __init__(self) -> None:
        self.pumpNumber = 6

    def getMissingIngredientNumber(self, cocktailId) -> int:
        cocktailInredients = cocktailsDB.getIngredientList(cocktailId)
        pumpList = ingredientsDB.getMotorList()
        for el in pumpList:
            if el["ingredient"] in cocktailInredients:
                cocktailInredients.remove(el["ingredient"])
        return len(cocktailInredients)

    def getMissingIngredients(self, cocktailId):
        cocktailInredients = cocktailsDB.getIngredientList(cocktailId)
        pumpList = ingredientsDB.getMotorList()
        for el in pumpList:
            if el["ingredient"] in cocktailInredients:
                cocktailInredients.remove(el["ingredient"])
        return cocktailInredients

    def getRightIngredients(self, cocktailId):
        cocktailInredients = cocktailsDB.getIngredientList(cocktailId)
        pumpList = ingredientsDB.getMotorList()
        newList = []
        for el in pumpList:
            if el["ingredient"] in cocktailInredients:
                newList.append(el)
        return newList

    def hijackCocktailData(self, data):
        for el in data:
            el["missing"] = self.getMissingIngredientNumber(el["id"])
        return data
