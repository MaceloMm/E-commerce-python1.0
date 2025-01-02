from _databases import DataBases
from datetime import datetime
from sqlite3 import DatabaseError

"""
1. Produto
- Atributos: id, nome, preco, quantidade.
- Métodos:
- adicionar_produto()
- editar_produto()
- remover_produto()
- listar_produtos()
"""

db = DataBases()

class Product:


    def __init__(self, name: str, price: int, quantity: int):
        self.__name = name
        self.__price = price
        self.__quantity = quantity


    def add_product(self):
        if self.__name is None or self.__price is None or self.__quantity is None:
            raise ValueError("Dados do produto invalidos!")
        
        cursor = db.get_cursor
        cursor.execute(
            """
            INSERT into Product (ProductName, ProductPrice, ProductQuantity, CreateAT, Alteration) VALUES
            (?, ?, ?, ?, ?);
            """, (
                self.__name, 
                self.__price, 
                self.__quantity,
                datetime.now().strftime("%Y/%m/%d - %H:%M:%S"),
                datetime.now().strftime("%Y/%m/%d - %H:%M:%S"))
        )

        db.commit_changes()
        db.close_connetion()
        
    @staticmethod
    def edit_product():
        Product.list_product()
        print()
        db = DataBases()

        def change_name():
            try:
                product_id = int(input("Digite o ID do produto que deseja alterar o nome: "))
                new_name = str(input("Digite o novo nome do produto: "))
                if not new_name:
                    print("O nome do produto não pode ser vazio.")
                    return
                cursor = db.get_cursor
                cursor.execute("UPDATE Product SET ProductName = ? WHERE ProductID = ?", (new_name, product_id))
                db.commit_changes()
                print("Nome do produto atualizado com sucesso!")

            except DatabaseError as Er:
                print(f"Erro no banco de dados {Er}")

            except Exception as Er:
                print(f"Erro ao atualizar o nome: {Er}")

        def change_price():
            try:
                product_id = int(input("Digite o ID do produto que deseja alterar o preço: "))
                new_price = int(input("Digite o novo preço do produto: "))
                if not new_price:
                    print("O preço do produto não pode ser vazio!")
                    return
                cursor = db.get_cursor
                cursor.execute("UPDATE Product SET ProductPrice = ? WHERE ProductID = ?", (new_price, product_id))
                db.commit_changes()
                print("Preço do produto atualizado com sucesso!")

            except DatabaseError as Er:
                print(f"Erro no banco de dados {Er}")

            except Exception as Er:
                print(f"Erro ao atualizar o preço: {Er}")

        def change_quantity():
            try:
                product_id = int(input("Digite o ID do produto que deseja alterar a quantidade: "))
                new_quantity = int(input("Digite a nova quantidade do produto: "))
                if not new_quantity:
                    print("A quantidade não pode ser vazio!")
                    return
                cursor = db.get_cursor
                cursor.execute("UPDATE Product SET ProductQuantity = ? WHERE ProductID = ?", (new_quantity, product_id))
                db.commit_changes()
                print("Quantidade do produto atualizada com sucesso!")

            except DatabaseError as Er:
                print(f"Erro no banco de dados {Er}")

            except Exception as Er:
                print(f"Erro ao atualizar a quantidade: {Er}")    
        
        # Menu de ações para edição dos produtos (teste)
        while True:
            choice = input("=== Menu === \n1) Nome \n2) Preço \n3) Quantidade \n4) Sair \nEscolha a opção que deseja alterar: ")
            if choice == "1":
                change_name()
            elif choice == "2":
                change_price()
            elif choice == "3":
                change_quantity()
            elif choice == "4":
                break
            else:
                print("Escolha inválida! Tente novamente.")

    def remove_product(self):
        pass
    
    @staticmethod
    def list_product():
        cursor = db.get_cursor
        cursor.execute("SELECT ProductID, ProductName, ProductPrice, ProductQuantity FROM Product;")
  
        result = cursor.fetchall()
        for res in result:
            print(f"ID: {res[0]}, Nome: {res[1]}, Preço: {res[2]}, Quantidade: {res[3]}")

        db.close_connetion()

        
if __name__ == "__main__":
    
    Product.edit_product()