from typing import List, Tuple
from src._databases import DataBases
from src._functions import set_time
import json
"""
3. Pedido
- Atributos: id, cliente_id, produtos, quantidades, total.
- Métodos:
- registrar_pedido()
- listar_pedidos()
- filtrar_pedidos()
"""


class Order:

    db = DataBases()
    cursor = db.get_cursor

    def __init__(self, client_id: int, produtcs: List[Tuple[str, int]], total: float) -> None:

        self.client_id = client_id
        self.products = produtcs
        self.total = total

    @property
    def client_id(self):
        return self.__client_id

    @client_id.setter
    def client_id(self, value: int):
        self.__client_id = value

    @property
    def products(self):
        return self.__products

    @products.setter
    def products(self, value: list):
        self.__products = value

    @property
    def total(self):
        return self.__total

    @total.setter
    def total(self, value: float):
        self.__total = value

    def insert_order(self) -> str:
        try:
            time = set_time()
            Order.cursor.execute(
               """
               INSERT INTO Orders (ClientID, TotalProducts, Total, CreateAT, Alteration) VALUES
               (?, ?, ?, ?, ?);
               """, (self.client_id, json.dumps(self.products), self.total, time, time)
            )
        except Order.db.exepitons_returns() as err:
            return f'Ocorreu um erro ao inserir o produto!'
        else:
            Order.db.commit_changes()
            return 'Pedido realizado com sucesso!'


if __name__ == '__main__':
    teste = Order(1, produtcs=[('Queijo', 2), ('Presunto', 3)], total=50.0)
    print(teste.insert_order())
