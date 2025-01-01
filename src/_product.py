"""
1. Produto
- Atributos: id, nome, preco, quantidade.
- Métodos:
- adicionar_produto()
- editar_produto()
- remover_produto()
- listar_produtos()
"""


class Product:

    counter_id = 0

    def __init__(self, name: str, price: int, quantity: int):
        self.__id = Product.counter_id + 1
        self.__name = name
        self.__price = price
        self.__quantity = quantity
        Product.counter_id = self.__id


    def add_product(self):
        pass

    def edit_product(self):
        pass

    def remove_product(self):
        pass

    def list_product(self):
        pass
