from src._functions import check_email, set_time
from src._databases import DataBases
import json

"""
- Atributos: id, nome, email, endereco.
- Métodos:
- adicionar_cliente()
- editar_cliente()
- remover_cliente()
- listar_clientes()
"""

db = DataBases()


class Client:

    cursor = db.get_cursor

    def __init__(self, name: str, email: str, adress: dict):
        self.__name = name
        if not check_email(email):
            raise ValueError('Email invalido')
        self.__email = email
        self.__endereco = adress

    def insert_client(self) -> str:

        if self.__name is None or self.__email is None or self.__endereco is None:
            raise ValueError('Dados do cliente invalidos!')

        emails = Client.cursor.execute(
            """
            SELECT ClientEmail FROM Client;
            """
        ).fetchall()

        if self.__email in (i[0] for i in emails):
            return 'Este email já foi cadastrado'

        creat_at = set_time()

        Client.cursor.execute(
            """
            INSERT into Client (ClientName, ClientEmail, ClientLocation, CreateAT, Alteration, Status) VALUES
            (?, ?, ?, ?, ?, ?);
            """, (
                self.__name,
                self.__email, json.dumps(self.__endereco),
                creat_at,
                creat_at,
                True)
        )

        db.commit_changes()

        return f'Usuário {self.__name} cadastrado com sucesso!'

    @staticmethod
    def edit_client(clientid: int, new_name: str = None, new_email: str = None, new_adress: dict = None) -> str:
        """
        Método responsavel por realizar as alterações dentro dos cadastros dos clientes.

        :param clientid: ID do cliente cadastrado no banco
        :param new_name: Parametro Opcional do metodo caso queira alterar o nome do cliente
        :param new_email: Parametro Opcional do metodo caso queira alterar o Email do cliente
        :param new_adress: Parametro Opcional do metodo caso queira alterar o endereço do cliente
        :return: Retorna um mensagem que a alteração foi realizada com sucesso.
        """

        if clientid <= 0:
            raise ValueError('ID de client invalido')

        # Gera um dicionario com as informações a serem alteradas.
        updates = {}
        if new_name:
            updates["ClientName"] = new_name
        if new_email:
            updates["ClientEmail"] = new_email
        if new_adress:
            updates["ClientLocation"] = json.dumps(new_adress)

        updates["Alteration"] = set_time()

        # caso nenhuma seja encontrada ira jogar um erro informando que nenhum campo foi preenchido
        if not updates:
            raise ValueError("Nenhum campo para atualizar foi fornecido")

        # O set_clause gera a parte do SET da querry fazendo a seguinte coisa (ClientName = ?, ClientEmail = ?)
        set_clause = ", ".join(f"{key} = ?" for key in updates.keys())

        # O values faz a mesma coisa que o set_clause, porém utiliza os valores transformando numa lista
        # ['Macelo Augusto', 'Macelo@macelo.com', 1]
        values = list(updates.values()) + [clientid]

        # Aqui realizamos a criação da querry
        query = f"UPDATE Client SET {set_clause} WHERE ClientID = ?;"
        Client.cursor.execute(query, values)

        db.commit_changes()

        return 'Alteração feita com sucesso!'

    @staticmethod
    def delete_client(clientid: int) -> str:

        if clientid <= 0:
            raise ValueError("ID do cliente invalido!")

        usuario = Client.search_client(clientid)

        Client.cursor.execute(
            """
            UPDATE Client SET Status = ? WHERE ClientID = ?;
            """, (
                False,
                clientid,
            )
        )

        db.commit_changes()

        return f'Cliente {usuario} deletado com sucesso!'

    @staticmethod
    def list_client(search_name: bool = False) -> list:

        if search_name:
            list_client = Client.cursor.execute(
                """
                SELECT ClientName FROM Client WHERE Status = True;
                """
            ).fetchall()

            return [name[0] for name in list_client]

        list_client = Client.cursor.execute(
            """
            SELECT ClientID, ClientName, ClientEmail, ClientLocation, Status FROM Client WHERE Status = True;
            """
        ).fetchall()

        return [cliente for cliente in list_client if cliente[4] == 1]

    @staticmethod
    def validation_client() -> bool:

        ids = Client.cursor.execute(
            """
            SELECT ClientID FROM Client;
            """
        ).fetchall()

        if ids:
            return True
        return False

    @staticmethod
    def search_client(clientid: int, dados=False) -> str:

        if dados:
            name_client = Client.cursor.execute(
                'SELECT ClientName, ClientEmail, ClientLocation FROM Client WHERE ClientID = ?;', (clientid,)
            )
        else:
            name_client = Client.cursor.execute(
                'SELECT ClientName FROM Client WHERE ClientID = ?', (clientid,)
            ).fetchone()[0]

        return name_client

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
    # cliente.insert_client()
    #cliente2 = Client('Luciana', 'luciana@gmail.com', {'CEP': 'teste', 'Rua': 'teste', 'Numero': 'teste'})
    #cliente2.insert_client()
    #print(Client.validation_client())
    # cliente.delete_client(1)
    print(list(Client.list_client()))
