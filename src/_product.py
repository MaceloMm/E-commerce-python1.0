from _databases import DataBases
from _functions import set_time

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

    cursor = db.get_cursor

    def __init__(self, name: str, price: int, quantity: int):
        self.__name = name
        self.__price = price
        self.__quantity = quantity

    # Método está OK
    def add_product(self):
        if self.__name is None or self.__price is None or self.__quantity is None:
            raise ValueError("Dados do produto invalidos!")
        
        creat_at = set_time()
        Product.cursor.execute(
            """
            INSERT into Product (ProductName, ProductPrice, ProductQuantity, CreateAT, Alteration) VALUES
            (?, ?, ?, ?, ?);
            """, (
                self.__name, 
                self.__price, 
                self.__quantity,
                creat_at,
                creat_at)
        )

        db.commit_changes()

        return f"Produto '{self.__name}' adicionado com sucesso!"

    # Método está OK    
    @staticmethod
    def edit_product(product_id: int, new_name: str = None, new_price: int = None, new_quantity: int = None) -> str:
        """
        Método responsável por realizar as alterações dentro dos cadastros dos produtos.

        :param product_id: ID do produto cadastrado no banco
        :param new_name: Parâmetro Opcional do método caso queira alterar o nome do produto
        :param new_price: Parâmetro Opcional do método caso queira alterar o preço do produto
        :param new_quantity: Parâmetro Opcional do método caso queira alterar a quantidade do produto em estoque
        :return: Retorna uma mensagem informando que a alteração foi realizada com sucesso
        """

        if product_id <= 0:
            raise ValueError("ID de produto inválido")
        
        updates = {}
        if new_name:
            updates["ProductName"] = new_name
        if new_price:
            updates["ProductPrice"] = new_price
        if new_quantity:
            updates["ProductQuantity"] = new_quantity

        updates["Alteration"] = set_time()

        if not updates:
            raise ValueError("Nenhum campo para atualizar foi fornecido")

        set_clause = ", ".join(f"{key} = ?" for key in updates.keys())
        values = list(updates.values()) + [product_id]

        query = f"UPDATE Product SET {set_clause} WHERE ProductID = ?;"
        Product.cursor.execute(query, values)

        db.commit_changes()

        return 'Alteração realizada com sucesso!'

    # Método está OK
    @staticmethod
    def delete_product(product_id: int) -> str:
        
        if product_id <= 0:
            raise ValueError("ID do produto inválido!")
        
        try:
            product = Product.cursor.execute(
                """
                SELECT ProductName from Product WHERE ProductID = ?
                """, (
                    product_id,
                )
            ).fetchone()[0]  
        # Essa exceção irá tratar casos em que o ID não existir no banco
        except TypeError:
            return f"Erro: O ID de produto '{product_id}' não existe!"

        Product.cursor.execute(
            """
            DELETE FROM Product WHERE ProductID = ?
            """, (
                product_id,
            )
        )

        db.commit_changes()

        return f"Produto '{product}' deletado com sucesso!"

    # Método está OK
    @staticmethod
    def list_product() -> list:
        
        result = Product.cursor.execute(
            "SELECT ProductID, ProductName, ProductPrice, ProductQuantity FROM Product;").fetchall()
        
        return list(result)

       
if __name__ == "__main__":
    Product.list_product()
    print(Product.list_product())
