
from src._functions import check_email

"""
- Atributos: id, nome, email, endereco.
- Métodos:
- adicionar_cliente()
- editar_cliente()
- remover_cliente()
- listar_clientes()
"""


class Client:

    def __init__(self, nome: str, email: str, endereco: dict):
        self.__name = nome
        if not check_email(email):
            raise ValueError('Email invalido')
        self.__email = email
        self.__endereco = endereco

    def insert_client(self):
        pass

    def edit_client(self):
        pass

    def delete_client(self):
        pass

    def list_client(self):
        pass

    @property
    def name(self):
        return self.__name

    @property
    def get_email(self):
        return self.__email

    @property
    def get_endereco(self):
        return self.__endereco

    @name.setter
    def name(self, name):
        self.__name = name

    def __str__(self):
        return f'<Class.Client: {self.__name}>'

    def __repr__(self):
        return f'<Class.Client: {self.__name}>'


# Apenas para testes
if __name__ == '__main__':
    cliente = Client('Macelo', 'Macelo@gmail.com', {'bairro': 'COHAB 2', 'Numero': '192', 'Rua': 'tatui', 'CEP': '06326-455'})

    print(cliente.name)
    cliente.name = 'Macelo Augusto'
    print(cliente.name)
