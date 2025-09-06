from tkinter import ttk, Menu
import customtkinter as tk
from src._functions import fonts, format_price
from src.services.product_service import ProductService
from tkinter import messagebox
from src.models._product import Product
from src.interface._imagens import IMAGE_BACK
from src.interface._imagens import IMAGE_SINGUP, IMAGE_DELETE, IMAGE_ALTERAR

ps = ProductService()
prod_id = 0


class ScreenProduct(tk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color='#1f1f1f')

        b_font, t_font, f_font = fonts()

        texto = tk.CTkLabel(self, text='Clientes cadastrados:', font=t_font)
        texto.pack(pady=10, anchor='w')

        table = ttk.Treeview(self, columns=("id", "Nome", "Preço", "Estoque"), show="headings")

        table.heading("id", text="ID")
        table.heading("Nome", text="Nome")
        table.heading("Preço", text="Preço")
        table.heading("Estoque", text="Estoque")

        table.column("id", width=50, anchor="center")
        table.column("Nome", width=100, anchor="center")
        table.column("Preço", width=150, anchor="center")
        table.column("Estoque", width=75, anchor="center")

        dados = ps.list_products().get('data')

        for prod_id, nome, price, quantity, category  in dados:
            table.insert(
                "", tk.END, values=(
                    prod_id,
                    nome.title(),
                    format_price(price),
                    quantity,
                ))

        table.bind('<Button-3>', self.show_context_menu)
        table.pack(fill=tk.BOTH, expand=True)

        frame_teste = tk.CTkFrame(self, fg_color='#1f1f1f')
        frame_teste.pack(pady=10)

        button_singup = tk.CTkButton(frame_teste, text='Cadastrar Produto', font=b_font,
                                     command=lambda: master.show_frame(RegisterScreenProduct),
                                     image=IMAGE_SINGUP
                                     )
        button_singup.grid(pady=10, row=3, column=0, padx=5)

        button_delete = tk.CTkButton(frame_teste, text='Deletar Produto', font=b_font,
                                     command=lambda: self.validation_delete(master),
                                     image=IMAGE_DELETE
                                     )
        button_delete.grid(pady=10, row=3, column=1, padx=5)

        button_alterar = tk.CTkButton(frame_teste, text='Alterar Produto', font=b_font,
                                      command=lambda: self.validation_alteration(master),
                                      image=IMAGE_ALTERAR
                                      )
        button_alterar.grid(pady=10, row=3, column=2, padx=5)

        button_back = tk.CTkButton(frame_teste, text='Voltar', font=b_font,
                                   command=lambda: master.show_frame(master.get_gerencial_screen()),
                                   image=IMAGE_BACK
                                   )
        button_back.grid(pady=10, row=3, column=3, padx=5)

        # button_info = master.get_button_info()
        # button_info.config(command=messagebox.showinfo('Teste1', 'Teste1 aaaaaaa'))

        def get_dados(event):
            global prod_id

            item_selecionado = table.selection()[0]
            prod_id = int(table.item(item_selecionado, 'values')[0])

        table.bind("<<TreeviewSelect>>", get_dados)

    def show_context_menu(self, event):
         menu = Menu(self, tearoff=0, bg="#1f1f1f", fg="#B0C4DE")
         menu.add_command(label='Editar', command=lambda: self.validation_alteration(self.master))
         menu.add_command(label='Deletar', command=lambda: self.validation_delete(self.master))
         menu.tk_popup(event.x_root, event.y_root)

    @staticmethod
    def validation_alteration(master):
        global prod_id
        if prod_id == 0:
            messagebox.showinfo('Info', 'Selecione um cliente!')
        else:
            master.show_frame(UpdateScreenProduct)

    @staticmethod
    def validation_delete(master):
         global prod_id
         if prod_id == 0:
             messagebox.showinfo('Info', 'Selecione um produto!')
         else:
             master.show_frame(DeleteScreenProduct)


class RegisterScreenProduct(tk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color='#1f1f1f')

        b_font, t_font, f_font = fonts()

        text_principal = tk.CTkLabel(self, text='Cadastro de Produto!', font=t_font)
        text_principal.grid(row=0, column=0, columnspan=9, pady=15)

        label_product_name = tk.CTkLabel(self, text='Nome:')
        label_product_name.grid(row=1, column=0, columnspan=1, sticky='w')

        entry_product_name = tk.CTkEntry(self, width=290, placeholder_text='Nome')
        entry_product_name.grid(row=2, column=0, columnspan=4, pady=5, sticky='w')

        label_product_category = tk.CTkLabel(self, text='Categoria:')
        label_product_category.grid(row=3, column=0, pady=5, columnspan=1, sticky='w')

        entry_product_category = tk.CTkEntry(self, width=290, placeholder_text='Categoria')
        entry_product_category.grid(row=4, column=0, pady=5, sticky='w', columnspan=4)

        label_product_price = tk.CTkLabel(self, text='Preço:')
        label_product_price.grid(row=5, column=0, pady=5, sticky='w')

        entry_product_price = tk.CTkEntry(self, placeholder_text='Preço')
        entry_product_price.grid(row=6, column=0, pady=5, sticky='w')

        label_product_quantity = tk.CTkLabel(self, text='Quantidade:')
        label_product_quantity.grid(row=5, column=1, pady=5, sticky='w', padx=5)

        entry_product_quantity = tk.CTkEntry(self, placeholder_text='Quantidade')
        entry_product_quantity.grid(row=6, column=1, pady=5, padx=5)

        button_send = tk.CTkButton(self, text='Enviar', font=b_font,
                                   command=lambda: get_dados(
                                       name=entry_product_name.get(),
                                       category=entry_product_category.get(),
                                       price=entry_product_price.get(),
                                       quantity=entry_product_quantity.get(),
                                       master=master
                                   ))
        button_send.grid(row=99, column=0, pady=15)

        button = tk.CTkButton(self, text='Voltar', font=b_font,
                              command=lambda: master.show_frame(ScreenProduct))
        button.grid(row=99, column=1, pady=15)

        def get_dados(name, category, price, quantity, master):
            if name == '' or category == '' or price == '' or quantity == '':
                messagebox.showinfo('Info', 'Preencha todos os campos')
                return None

            try:
                response = ps.insert_product(Product(name=name, price=float(price), quantity=int(quantity), category=category))
            except ValueError as err:
                messagebox.showerror('Info', message=str(err))
            else:
                print(response)
                if response.get('success'):
                    messagebox.showinfo('Info', message=response.get('message'))
                else:
                    messagebox.showerror('Error', message=response.get('message'))
                master.show_frame(ScreenProduct)


class DeleteScreenProduct(tk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color='#1f1f1f')

        b_font, t_font, f_font = fonts()

        global prod_id
        name_client = ps.list_products(ProductID=prod_id).get('data')[0][1]

        label = tk.CTkLabel(self, text=f'Tem certeza que deseja deletar o produto "{name_client}"?')
        label.grid(row=0, column=0, columnspan=2, pady=15)

        button_yes = tk.CTkButton(self, text='Sim', font=b_font,
                                  command=lambda: delete_client(prod_id, master))
        button_yes.grid(row=1, column=0)

        button_no = tk.CTkButton(self, text='Não', font=b_font,
                                 command=lambda: back_screen(master))
        button_no.grid(row=1, column=1)

        def delete_client(p_id, master):
            global prod_id
            msg = ps.disable_product(product_id=p_id).get('message')
            messagebox.showinfo('Info', message=msg)
            prod_id = 0
            master.show_frame(ScreenProduct)

        def back_screen(master):
            global prod_id
            prod_id = 0
            master.show_frame(ScreenProduct)


class UpdateScreenProduct(tk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        global prod_id

        b_font, t_font, f_font = fonts()

        prod = ps.list_products(ProductID=prod_id).get('data')[0]
        prod = Product(name=prod[1], price=prod[2], quantity=prod[3], category=prod[4])

        text_principal = tk.CTkLabel(self, text='Alteração de cadastro!', font=tk.CTkFont('Arial', 20, 'bold'))
        text_principal.grid(row=0, column=0, columnspan=9, pady=15)

        label_product_name = tk.CTkLabel(self, text=f'Nome atual: {prod.name}', font=f_font)
        label_product_name.grid(row=1, column=0, columnspan=2, sticky='w', pady=10)

        entry_product_name = tk.CTkEntry(self, width=290)
        entry_product_name.grid(row=2, column=0, columnspan=2, pady=5, sticky='w')

        label_product_category = tk.CTkLabel(self, text=f'Categoria atual: {prod.category}', font=f_font)
        label_product_category.grid(row=3, column=0, pady=10, columnspan=2, sticky='w',)

        entry_product_category = tk.CTkEntry(self, width=290)
        entry_product_category.grid(row=4, column=0, pady=5, sticky='w', columnspan=2)

        label_product_price = tk.CTkLabel(self, text=f'Preço atual: {prod.price}', font=f_font)
        label_product_price.grid(row=5, column=0, pady=10, sticky='w')

        entry_product_price = tk.CTkEntry(self)
        entry_product_price.grid(row=6, column=0, pady=5, sticky='w')

        label_product_quantity = tk.CTkLabel(self, text=f'Quantidade atual: {prod.quantity}', font=f_font)
        label_product_quantity.grid(row=5, column=1, pady=10, sticky='w', padx=5)

        entry_product_quantity = tk.CTkEntry(self)
        entry_product_quantity.grid(row=6, column=1, pady=5, padx=5)

        button_send = tk.CTkButton(self, text='Alterar', font=b_font,
                                command=lambda: change_product(
                                    master,
                                    entry_product_name.get(),
                                    entry_product_category.get(),
                                    entry_product_price.get(),
                                    entry_product_quantity.get()
                                ))
        button_send.grid(row=99, column=0, pady=15)

        button = tk.CTkButton(self, text='Voltar', font=b_font,
                           command=lambda: back_screen(master))
        button.grid(row=99, column=1, pady=15)

        button_info = master.get_button_info()

        button_info.configure(command=lambda: messagebox.showinfo('Teste', 'Teste'))

        def change_product(master, new_name, new_category, new_price, new_quantity):
            global prod_id

            if new_name == '' and new_category == '' and new_price == '' and new_quantity == '':
                messagebox.showinfo('Info', 'Nenhum campo preenchido!')
                return None

            new_name = new_name if new_name != '' else None
            new_category = new_category if new_category != '' else None
            new_price = new_price if new_price != '' else None
            new_quantity = new_quantity if new_quantity != '' else None

            msg = ps.update_product(prod_id, ProductName=new_name, Category=new_category,
                                    ProductPrice=new_price, ProductQuantity=new_quantity).get('message')

            messagebox.showinfo('Info', msg)
            prod_id = 0
            master.show_frame(ScreenProduct)

        def back_screen(master):
            global prod_id
            prod_id = 0
            master.show_frame(ScreenProduct)