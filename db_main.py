import sqlite3
from db_cocktail_functions import Cocktails
from db_ingredients_functions import Ingredients


class Database():

    def __init__(self) -> None:
        self.connection = sqlite3.connect('database.db')
        # Add ingredient arr to this table
        self.sql_cocktail_table = """ CREATE TABLE IF NOT EXISTS cocktails (
                                            id integer PRIMARY KEY,
                                            title text NOT NULL,
                                            description text,
                                            img text,
                                            ingredients text NOT NULL,
                                            favorite integer
                                        ); """
        self.sql_all_ingredients_table = """ CREATE TABLE IF NOT EXISTS ingredients (
                                            id integer PRIMARY KEY,
                                            ingredient text NOT NULL UNIQUE,
                                            pump integer UNIQUE
                                        ); """
        self.create_table(self.sql_cocktail_table)
        self.create_table(self.sql_all_ingredients_table)

    def create_table(self, create_table_sql):
        try:
            c = self.connection.cursor()
            c.execute(create_table_sql)
        except Exception as e:
            print(e)

    def getCocktailDb(self):
        return Cocktails(self.connection)

    def getIngredientsDb(self):
        return Ingredients(self.connection)
