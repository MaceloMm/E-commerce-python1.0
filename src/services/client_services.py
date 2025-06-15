from src.repository.actions import Repository
from src.models._client import Client
import json


class ClientService:

    def __init__(self):
        self.table = 'Client'
        self.rep = Repository()

    def check_client(self, client_id: int = None, by_email: bool = False, **kwargs) -> dict:
        try:
            if by_email:
                response = self.rep.select(table=self.table, filters=True, ClientName=kwargs.get('email'))
            else:
                response = self.rep.select(table=self.table, filters=True, ClientID=client_id)
        except Exception as err:
            return {'success': False, 'message': 'Ocorreu um erro ao consultar o usuario', 'error': err}
        else:
            if not response:
                return {'success': True, 'exists': False, 'error': None}
            return {'success': True, 'exists': True, 'error': None}

    def insert_client(self, client: Client) -> dict:
        try:
            if self.check_client(by_email=True, email=client.email).get('exists'):
                return {'success': True, 'message': 'Usuario já está cadastrado', 'error': None}
            self.rep.insert(table=self.table, values=[client.name, client.email, json.dumps(client.address)])
        except Exception as err:
            return {'success': False, 'message': 'Ocorreu um erro ao inserir o usuario', 'error': err}
        else:
            return {'success': True, 'message': 'Usuario inserido com sucesso', 'error': None}

    def list_client(self, **kwargs) -> dict:
        try:
            if kwargs:
                response = self.rep.select(table=self.table, filters=True, **kwargs)
            else:
                response = self.rep.select(table=self.table)
        except Exception as err:
            return {'success': False, 'data': None, 'error': err}
        else:
            return {'success': True, 'data': response, 'error': None}

    def disable_client(self, client_id: int):
        """

        :param client_id:
        :return:
        """
        try:
            if not self.check_client(client_id=client_id).get('exists'):
                return {'success': False, 'message': 'Cliente não encontrado', 'error': None}
            self.rep.delete(table=self.table, delete_id=client_id)
        except Exception as err:
            return {'success': False, 'message': 'Ocorreu um erro ao desativar o cliente', 'error': err}
        else:
            return {'success': True, 'message': 'Cliente desativado com sucesso', 'error': None}

    def update_product(self, client_id: int, **kwargs) -> dict:
        try:
            if not self.check_client(client_id=client_id).get('exists'):
                return {'success': True, 'message': 'Não encontramos o cliente com id informado', 'error': None}
            self.rep.update(table=self.table, change_id=client_id, **kwargs)
        except Exception as err:
            return {'success': False, 'message': 'Ocorreu um erro ao atualizar o cliente', 'error': err}
        else:
            return {'success': True, 'message': 'Cliente atualizado com sucesso', 'error': None}


if __name__ == '__main__':
    cs = ClientService()
    cli = Client('Macelo', 'macelo@macelo.com',
                {'cep': '06326-455', 'logradouro': 'Rua Tatuí', 'bairro': 'Conjunto Habitacional Presidente Castelo Branco',
                  'localidade': 'Carapicuíba', 'uf': 'SP', 'estado': 'São Paulo'})
    cs.insert_client(cli)
    #print(cs.update_product(client_id=1, ClientName='Macelo Augusto'))
    #print(cs.disable_client(client_id=1))
    #print(cs.list_client(ClientEmail='macelo@macelo.com'))
