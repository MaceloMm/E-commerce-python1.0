"""
3. Pedido
- Atributos: id, cliente_id, produtos, quantidades, total.
- Métodos:
- registrar_pedido()
- listar_pedidos()
- filtrar_pedidos()
"""


class Order:

    def __init__(self, clientid: int, produtcs: list, quantity: int, total: float):

        self.__clientid = clientid
        self.__products = produtcs
        self.__quantity = quantity
        self.__total = total