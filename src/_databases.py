import os.path
import sqlite3
import sqlite3 as sql


class DataBases:

    def __init__(self):
        db_path = os.path.join(
            os.getcwd().replace('interface', '').replace('src', ''), 'databases\\commerce.db')
        self.__conn = sql.connect(db_path)
        self.create_table()
        self.create_types()

    def create_table(self) -> None:
        """

        :return: None
        """

        self.__conn.execute("PRAGMA foreign_keys = ON")

        cursor = self.get_cursor

        # Tabela de produtos
        cursor.execute(
            """
            CREATE TABLE if not exists Product(
            ProductID INTEGER primary key autoincrement,
            ProductName TEXT NOT NULL,
            ProductPrice REAL NOT NULL,
            ProductQuantity INTEGER NOT NULL,
            Category TEXT NOT NULL, 
            CreateAT TEXT NOT NULL,
            Alteration TEXT NOT NULL,
            Status BOOL NOT NULL
            );
            """
        )

        # Tabela de Clientes
        cursor.execute(
            """
            CREATE TABLE if not exists Client(
            ClientID INTEGER primary key autoincrement,
            ClientName TEXT NOT NULL,
            ClientEmail TEXT NOT NULL,
            ClientLocation TEXT NOT NULL,
            CreateAT TEXT NOT NULL,
            Alteration TEXT NOT NULL,
            Status BOOL NOT NULL
            );
            """
        )

        # Tabela de Pedidos
        cursor.execute(
            """
            CREATE TABLE if not exists Orders(
            OrderID INTEGER primary key autoincrement,
            ClientID INTEGER NOT NULL,
            TotalProducts TEXT NOT NULL,
            Total REAL,
            CreateAT TEXT NOT NULL,
            Alteration TEXT NOT NULL,
            FOREIGN KEY (ClientID) REFERENCES TypeUsers (ClientID) ON DELETE CASCADE 
            );
            """
        )

        # Tabela de Users
        cursor.execute(
            """
            CREATE TABLE if not exists users(
            UserID INTEGER primary key autoincrement,
            UserEmail TEXT NOT NULL UNIQUE, 
            UserPassword TEXT NOT NULL,
            Status BOOL NOT NULL,
            TypeID INTEGER NOT NULL,
            CreateAT TEXT NOT NULL,
            Alteration TEXT NOT NULL,
            FOREIGN KEY (TypeID) REFERENCES TypeUsers (TypeID) ON DELETE CASCADE
            );
            """
        )

        # Tabela tipos de usuarios
        cursor.execute(
            """
            CREATE TABLE if not exists TypeUsers(
            TypeName TEXT NOT NULL,
            TypeID INTEGER primary key autoincrement
            )
            """
        )

    def close_connetion(self):
        self.__conn.close()

    def commit_changes(self):
        self.__conn.commit()

    @property
    def get_cursor(self):
        return self.__conn.cursor()

    def create_types(self):
        cursor = self.get_cursor

        cadastro = cursor.execute(
            """
            SELECT count(TypeID) from TypeUsers;
            """
        ).fetchone()

        if cadastro[0] == 3:
            pass
        else:
            cursor.execute(
                """
                INSERT INTO TypeUsers (TypeName) 
                VALUES ("admin"), ("client"), ("gerente");
                """
            )
            self.commit_changes()

    @staticmethod
    def exepitons_returns():
        return (
            sqlite3.OperationalError, sqlite3.IntegrityError, sqlite3.ProgrammingError, sqlite3.InterfaceError,
            sqlite3.DatabaseError, sqlite3.DataError, sqlite3.NotSupportedError, sqlite3.Warning
        )



if __name__ == "__main__":
    db = DataBases()
    db.create_table()
