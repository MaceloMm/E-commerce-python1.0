from _databases import DataBases
from datetime import datetime

"""
1. Produto
- Atributos: id, nome, preco, quantidade.
- Métodos:
- adicionar_produto()
- editar_produto()
- remover_produto()
- listar_produtos()
"""

db = DataBases()

class Product:


    def __init__(self, name: str, price: int, quantity: int):
        self.__name = name
        self.__price = price
        self.__quantity = quantity


    def add_product(self):
        if self.__name is None or self.__price is None or self.__quantity is None:
            raise ValueError("Dados do produto invalidos!")
        
        cursor = db.get_cursor
        cursor.execute(
            """
            INSERT into Product (ProductName, ProductPrice, ProductQuantity, CreateAT, Alteration) VALUES
            (?, ?, ?, ?, ?);
            """, (
                self.__name, 
                self.__price, 
                self.__quantity,
                datetime.now().strftime("%Y/%m/%d - %H:%M:%S"),
                datetime.now().strftime("%Y/%m/%d - %H:%M:%S"))
        )

        db.commit_changes()

        db.close_connetion()
        

    def edit_product(self):
        pass

    def remove_product(self):
        pass

    def list_product(self):
        pass


if __name__ == "__main__":
    p1 = Product("Coca-cola", 10, 100)

    p1.add_product()