from src._databases import DataBases
from src._functions import set_time
from src._functions import format_adress
from typing import List
import json


class Repository:

    def __init__(self):
        self.db = DataBases()
        self.c_tables = {'Product': ['ProductID', 'ProductName', 'ProductPrice', 'ProductQuantity', 'Category'],
        'Client': ['ClientID', 'ClientName', 'ClientEmail', 'ClientLocation'],
        'Orders': ['OrderID', 'ClientID', 'TotalProducts', 'Total']
        }


    def insert(self, table: str, values: list):
        """
        Metódo responsavel por realizar a inserção de objetos dentro do banco.

        :param table: Informa a tabela que será realizada a ação
        :param values: informa um valor em listas de acordo com as colunas da tabela
            Exemplo:
            ('ProductName', 'ProductPrice', 'ProductQuantity', 'Category') = ['Produto Teste', 20, 10, 'Teste']
        :return: None
        """
        try:
            camps = [i for i in self.c_tables[table] if self.c_tables[table].index(i) != 0]
            camps.extend(['CreateAT', 'Alteration', 'Status'])
            values.extend([set_time(), set_time(), 1])
            query = f'INSERT INTO {table} {tuple(camps)} VALUES {tuple(values)}'
            self.db.get_cursor.execute(query)
        except self.db.exepitons_returns() as err:
            raise err
        else:
            self.db.commit_changes()

    def update(self, table: str, change_id: int, **kwargs):
        """
        Metodo responsavel por realizar alterações nos cadastros


        :param table: Nome da tabela que irá ser atualizada
        :param change_id: ID do objeto que será alterado
        :param kwargs: Informa os valores que e para alterar dentro da tabela.

            Exemplo:

            tabela de produtos "['ProductID', 'ProductName', 'ProductPrice', 'ProductQuantity', 'Category']":
            ProductName='Exemplo2', ProductPrice=40

            Lembrando que tem que ser o nome da tabela de acordo com o c_tables
        :return: None
        """
        try:
            camps = (i for i in self.c_tables[table] if self.c_tables[table].index(i) != 0)
            camp_id = self.c_tables[table][0]
            if 'Status' in kwargs.keys():
                kwargs['Status'] = 1 if kwargs['Status'] else 0
            update = ', '.join([f"{i} = '{kwargs[i]}'" for i in camps if i in kwargs and kwargs[i] is not None])
            print(f'{update = }')
            update += f', Alteration = "{set_time()}"'
            querry = f'UPDATE {table} SET {update} WHERE {camp_id} = {change_id}'
            print(f'{querry = }')
            self.db.get_cursor.execute(querry)
        except self.db.exepitons_returns() as err:
            raise err
        else:
            self.db.commit_changes()

    def select(self, table: str, filters=False, **kwargs) -> List[tuple]:
        """
        Metódo responsavel por realizar consultas dentro do banco de acordo com a tabela.

        :param table: Informa a tabela que será realizada a ação
        :param filters: Informa True caso for utilizar filtros na consulta.
        :param kwargs: Caso utilize filtros na consulta, informa qual campo deseja filtrar e o valor, lembrando que e
        de acordo com a tabela, exemplo:

            Tabela de Produtos: ['ProductName', 'ProductPrice', 'ProductQuantity', 'Category'], ProductName='Exemplo'
            irá filtrar todos os produtos que chamam exemplo
        :return: Retorna os valores encontrados na consulta.
        """
        try:
            if filters:
                filter_camps = ' AND '.join([f'{i} = "{kwargs[i]}"' for i in self.c_tables[table] if i in kwargs])
                return self.db.get_cursor.execute(f"""SELECT {','.join(self.c_tables[table])} FROM {table} WHERE status = ? AND {filter_camps};""",
                                                  (True, )).fetchall()
            return self.db.get_cursor.execute(f"""
                SELECT {','.join(self.c_tables[table])} FROM {table} WHERE status = ?
            """, (True, )).fetchall()
        except self.db.exepitons_returns() as err:
            raise err
        except Exception as err:
            return err

    def delete(self, table: str, delete_id: int):
        """
        Metodo responsavel por realizar alteração no status do objeto dentro do banco

        :param table: Tabela que será realizada a alteração
        :param delete_id: ID do elemento que irá ser desativado
        :return: None
        """
        try:
            self.db.get_cursor.execute(f"""
            UPDATE {table} SET Status = ?, Alteration = ? WHERE {self.c_tables[table][0]} = ?;
            """, (False, set_time(), delete_id))
        except self.db.exepitons_returns() as err:
            raise err
        else:
            self.db.commit_changes()

if __name__ == '__main__':
    rep = Repository()
    address = json.dumps(format_adress({"cep": "06326-455", "logradouro": "Rua Tatu\\u00ed", "bairro": "Conjunto Habitacional Presidente Castelo Branco", "localidade": "Carapicu\\u00edba", "uf": "SP", "estado": "S\\u00e3o Paulo"}, 192))
    # rep.update('Client', 1, ClientLocation=address)
    # rep.insert('Product', ('Teste3', 50, 20, 'Teste', set_time(), set_time(), True))
    print(json.loads(rep.select(table='Client', filters=True, ClientID=1)[0][3]))
