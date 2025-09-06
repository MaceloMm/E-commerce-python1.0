from src.repository.actions import Repository
from src.models._product import Product
from typing import Union


class ProductService:

    def __init__(self):
        self.rep = Repository()
        self.table = 'Product'

    def check_product(self, product_id: int = None, by_name: bool = False, **kwargs) -> dict:
        """
        Função responsavel por verificar se um cadastro existe dentro do banco.

        :param product_id: Recebe o id para realizar a consulta no banco.
        :param by_name: informa True caso queira realizar a consulta pelo o nome.
        :param kwargs: informa o argumento name='Exemplo' para verificar se o nome existe no banco.
        :return: Retorna uma resposta informando se houve sucesso na consulta e se existe ou não o cliente, através de
        um dicionario.
        """
        try:
            if by_name:
                response = self.rep.select(table=self.table, ProductName=kwargs['name'], filters=True)
            else:
                response = self.rep.select(table=self.table, ProductID=product_id, filters=True)
        except Exception as err:
            return {'success': False, 'message': 'correu um erro ao consultar o banco', 'error': err}
        else:
            if response:
                return {'success': True, 'exists': True, 'error': None}
            return {'success': True, 'exists': False, 'error': None}

    def insert_product(self, product: Product) -> dict:
        """

        :param product:
        :return:
        """
        try:
            if self.check_product(by_name=True, name=product.name).get('exists'):
                return {'success': True, 'message': 'Produto já cadastrado no sistema', 'error': None}
            response = self.rep.insert(table=self.table, values=[product.name, product.price, product.quantity, product.category])
        except Exception as err:
            return {'success': False, 'message': 'Ocorreu um erro ao inserir o produto', 'error': err}
        else:
            return {'success': True, 'message': 'Produto cadastrado com sucesso', 'error': None}

    def list_products(self, **kwargs) -> dict:
        """

        :param kwargs:
        :return:
        """
        try:
            if kwargs:
                response = self.rep.select(table=self.table, filters=True, **kwargs)
            else:
                response = self.rep.select(table=self.table)
        except Exception as err:
            return {'success': False, 'message': 'correu um erro ao consultar o banco', 'error': err}
        else:
            return {'success': True, 'data': response if response else [], 'error': None}

    def disable_product(self, product_id: int):
        """

        :param product_id:
        :return:
        """
        try:
            if not self.check_product(product_id=product_id).get('exists'):
                return {'success': False, 'message': 'Produto não encontrado', 'error': None}
            self.rep.delete(table=self.table, delete_id=product_id)
        except Exception as err:
            return {'success': False, 'message': 'Ocorreu um erro ao desativar o produto', 'error': err}
        else:
            return {'success': True, 'message': 'Produto desativado com sucesso', 'error': None}

    def update_product(self, product_id: int, **kwargs) -> dict:
        try:
            if not self.check_product(product_id=product_id).get('exists'):
                return {'success': True, 'message': 'Não encontramos o produto com id informado', 'error': None}
            self.rep.update(table=self.table, change_id=product_id, **kwargs)
        except Exception as err:
            return {'success': False, 'message': 'Ocorreu um erro ao atualizar o produto', 'error': err}
        else:
            return {'success': True, 'message': 'Produto atualizado com sucesso', 'error': None}


if __name__ == '__main__':
    ps = ProductService()
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
        ps.insert_product(Product(i[0], int(i[1]), int(i[2]), i[3]))
    # print(ps.check_product(by_name=True, name='Micro-ondas'))
    print(ps.list_products())