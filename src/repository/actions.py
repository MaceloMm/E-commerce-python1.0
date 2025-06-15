from src._databases import DataBases
from src._functions import set_time
from typing import List


class Repository:

    def __init__(self):
        self.db = DataBases()
        self.c_tables = {'Product': ['ProductID', 'ProductName', 'ProductPrice', 'ProductQuantity', 'Category'],
        'Client': ['ClientID', 'ClientName', 'ClientEmail', 'ClientLocation'],
        'Orders': ['OrderID', 'ClientID', 'TotalProducts', 'Total']
        }


    def insert(self, table: str, values: list):
        """
        Metódo responsavel 

        :param table:
        :param values:
        :return:
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
        :param kwargs: Informa os valores que e para enviar exemplo name='Teste'
        :return: Retorna NONE ou um erro caso ocorra problema com o banco
        """
        try:
            camps = self.c_tables[table]
            camp_id = camps.pop(0)
            if 'Status' in kwargs.keys():
                kwargs['Status'] = 1 if kwargs['Status'] else 0
            update = ', '.join([f'{i} = "{kwargs[i]}"' for i in camps if i in kwargs])
            update += f', Alteration = "{set_time()}"'
            querry = f'UPDATE {table} SET {update} WHERE {camp_id} = {change_id}'
            self.db.get_cursor.execute(querry)
        except self.db.exepitons_returns() as err:
            raise err
        else:
            self.db.commit_changes()

    def select(self, table: str, filters=False, **kwargs) -> List[tuple]:
        """

        :param table:
        :param filters:
        :param kwargs:
        :return: None
        """
        try:
            if filters:
                filter_camps = ' AND '.join([f'{i} = "{kwargs[i]}"' for i in self.c_tables[table] if i in kwargs])
                return self.db.get_cursor.execute(f"""SELECT * FROM {table} WHERE status = ? AND {filter_camps};""",
                                                  (True, )).fetchall()
            return self.db.get_cursor.execute(f"""
                SELECT * FROM {table} WHERE status = ?
            """, (True, )).fetchall()
        except self.db.exepitons_returns() as err:
            raise err
        except Exception as err:
            return err

    def delete(self, table: str, delete_id: int):
        """
        Metodo responsavel por realizar alteração no status do objeto dentro do banco

        :param table: Tabela que será realizada a alteração
        :param delete_id: ID do elemento que irá ser alterado
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
    rep.update('Product', 21, Status=True)
    # rep.insert('Product', ('Teste3', 50, 20, 'Teste', set_time(), set_time(), True))
