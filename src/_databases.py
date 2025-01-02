import os.path
import sqlite3 as sql


class DataBases:

    def __init__(self):

        db_path = os.path.join(os.getcwd().replace('src', 'databases\\'), 'commerce.db')
        self.__conn = sql.connect(db_path)
        self.create_table()

    def create_table(self):
        """

        :return:
        """

        cursor = self.get_cursor

        # Tabela de produtos
        cursor.execute(
            """
            CREATE TABLE if not exists Product(
            ProductID INTEGER primary key autoincrement,
            ProductName TEXT,
            ProductPrice REAL,
            ProductQuantity INTEGER, 
            CreateAT TEXT,
            Alteration TEXT);
            """
        )

        # Tabela de Clientes
        cursor.execute(
            """
            CREATE TABLE if not exists Client(
            ClientID INTEGER primary key autoincrement,
            ClientName TEXT,
            ClientEmail TEXT,
            ClientLocation TEXT,
            CreateAT TEXT,
            Alteration TEXT);
            """
        )

        # Tabela de Pedidos
        cursor.execute(
            """
            
            """
        )

    def close_connetion(self):
        self.__conn.close()

    def commit_changes(self):
        self.__conn.commit()

    @property
    def get_cursor(self):
        return self.__conn.cursor()


if __name__ == "__main__":
    db = DataBases()
    db.create_table()
