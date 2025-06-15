from mypy.stubutil import report_missing

from src.repository.actions import Repository
from src.models._order import Order
import json


class OrderService:

    def __init__(self):
        self.rep = Repository()
        self.table = 'Orders'

    def check_order(self, order_id) -> dict:
        try:
            response = self.rep.select(table=self.table, filters=True, OrderID=order_id)
        except Exception as err:
            return {'success': False, 'exists': None, 'error': err}
        else:
            if response:
                return {'success': True, 'exists': True, 'error': None}
            return {'success': True, 'exists': False, 'error': None}

    def insert_order(self, order: Order) -> dict:
        try:
            self.rep.insert(table=self.table, values=[order.client_id, order.products, order.total])
        except Exception as err:
            return {'success': False, 'message': 'Ocorreu um erro ao criar a order', 'error': err}
        else:
            return {'success': True, 'message': 'Pedido criado com sucesso', 'error': None}

    def cancel_order(self, order_id: int) -> dict:
        try:
            if not self.check_order(order_id).get('exists'):
                return {'success': True, 'message': 'Order não encontrada', 'error': None}
            self.rep.delete(table=self.table, delete_id=order_id)
        except Exception as err:
            return {'success': False, 'message': 'Ocorreu um erro ao cancelar a order', 'error': err}
        else:
            return {'success': True, 'message': 'Order desativada com sucesso', 'error': None}

    def select_orders(self, by_client: bool = False, client_id: int = None) -> dict:
        try:
            if by_client:
                response = self.rep.select(table=self.table, filters=True, ClientID=client_id)
            else:
                response = self.rep.select(table=self.table)
        except Exception as err:
            return {'success': False, 'data': None, 'error': err}
        else:
            return {'success': True, 'data': response, 'error': None}

if __name__ == '__main__':
    ors = OrderService()

