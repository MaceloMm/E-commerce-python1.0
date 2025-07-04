from src._databases import DataBases
from src._functions import set_time

"""
1. Produto
- Atributos: id, nome, preco, quantidade, categoria, data de criação, data de modificação, status.
- Métodos:
- adicionar_produto()
- editar_produto()
- remover_produto()
- listar_produtos()
- verificar_produto()
"""

db = DataBases()


class Product:

    cursor = db.get_cursor

    def __init__(self, name: str, price: int, quantity: int, category: str):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError('Nome não pode ficar vazio')
        self.__name = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value: int):
        if value <= 0:
            raise ValueError('O preço precisa ser maior que 0')
        self.__price = value

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, value: int):
        if value < 0:
            raise ValueError('Quantidade tem que maior ou igual a 0')
        self.__quantity = value

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, value: str):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError('Categoria não pode ficar vazio')
        self.__category = value

    # Método está OK
    def add_product(self):
        if self.name is None or self.price is None or self.quantity is None or self.category is None:
            raise ValueError("Dados do produto invalidos!")
        
        creat_at = set_time()
        Product.cursor.execute(
            """
            INSERT into Product (ProductName, ProductPrice, ProductQuantity, Category, CreateAT, Alteration, Status) VALUES
            (?, ?, ?, ?, ?, ?, ?);
            """, (
                self.name,
                self.price,
                self.quantity,
                self.category,
                creat_at,
                creat_at,
                True)
        )

        db.commit_changes()

        return f"Produto '{self.name}' adicionado com sucesso!"

    # Método está OK    
    @staticmethod
    def edit_product(product_id: int, new_name: str = None, new_price: int = None, new_quantity: int = None, new_category: str = None) -> str:
        """
        Método responsável por realizar as alterações dentro dos cadastros dos produtos.

        :param product_id: ID do produto cadastrado no banco
        :param new_name: Parâmetro Opcional do método caso queira alterar o nome do produto
        :param new_price: Parâmetro Opcional do método caso queira alterar o preço do produto
        :param new_quantity: Parâmetro Opcional do método caso queira alterar a quantidade do produto em estoque
        :param new_category: Parâmetro Opcional do método caso queira alterar a categoria do produto
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
        if new_category:
            updates["Category"] = new_category

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
        
        product = Product.check_product(product_id)

        if product:
            Product.cursor.execute(
                """
                UPDATE Product SET Status = False WHERE ProductID = ?
                """, (
                    product_id,
                )
            )

            db.commit_changes()

            return f"Produto '{product}' deletado com sucesso!"
        return f"ID de produto '{product_id}' inexistente!"

    # Método está OK
    @staticmethod
    def list_product(category: str = None, seach_name: bool = False) -> list:
        """
        Método responsável por listar os produtos ativos no sistema

        :param category: Parametro responsável por filtrar a lista de produtos por determinada categoria
        :param seach_name:
        :return: Retorna uma lista de tuplas com as informações dos produtos ativos no sistema
        """

        if seach_name:
            result = Product.cursor.execute(
                """
                SELECT ProductName From Product Where Status = True;
                """
            ).fetchall()

            return [name[0] for name in result]
        
        if category:
            result = Product.cursor.execute(
            "SELECT ProductID, ProductName, ProductPrice, ProductQuantity FROM Product WHERE Status = True AND Category = ?", (category,)).fetchall()

            return list(result)
        
        result = Product.cursor.execute(
            "SELECT ProductID, ProductName, ProductPrice, ProductQuantity FROM Product WHERE Status = True;"
            ).fetchall()
        
        return list(result)

    # Método está OK
    @staticmethod
    def check_product(product_id: int) -> str:
        """
        Método responsável verificar se o ID do produto é válido em uma consulta no banco de dados.

        :param product_id: ID do produto cadastrado no banco
        :return: Retorna o nome do produto com base no ID passado como parâmetro
        """
        
        active_products = Product.list_product()

        if product_id <= 0 or product_id not in [product[0] for product in active_products]:
            raise ValueError(f"ID do produto inválido: {product_id}")
        
        return [product[1] for product in active_products if product[0] == product_id][0]
        

if __name__ == "__main__":
    produtos = [
        ['Tablet', '1800', '15', 'Eletrônicos'],
        ['Impressora Multifuncional', '600', '10', 'Informática'],
        ['Headset Gamer', '350', '20', 'Áudio'],
        ['Micro-ondas', '900', '12', 'Eletrodomésticos'],
        ['Câmera de Segurança', '450', '18', 'Eletrônicos'],
        ['HD Externo 1TB', '400', '25', 'Informática'],
        ['Liquidificador', '250', '30', 'Eletrodomésticos'],
        ['Console de Videogame', '4500', '5', 'Eletrônicos'],
        ['Mousepad RGB', '150', '40', 'Informática'],
        ['Carregador Portátil', '220', '22', 'Eletrônicos'],
    ]

    for i in produtos:
        p = Product(name=i[0], price=int(i[1]), quantity=int(i[2]), category=i[3])
        print(p.add_product())
        print('Script Finalizado')
    for i in Product.list_product():
        print(i)


