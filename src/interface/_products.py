from tkinter import ttk
import customtkinter as tk
from src._functions import fonts, format_price
from src._product import Product
from src.interface._imagens import IMAGE_BACK, IMAGE_ALTERAR, IMAGE_DELETE


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

        dados = Product.list_product()

        for cl_id, nome, price, storage in dados:
            table.insert(
                "", tk.END, values=(
                    cl_id,
                    nome.title(),
                    format_price(price),
                    storage,
                ))

        # table.bind('<Button-3>', self.show_context_menu)
        table.pack(fill=tk.BOTH, expand=True)

        frame_teste = tk.CTkFrame(self, fg_color='#1f1f1f')
        frame_teste.pack(pady=10)

        button_singup = tk.CTkButton(frame_teste, text='Cadastrar Produto', font=b_font,
                                     # command=lambda: master.show_frame(RegisterClientScreen),
                                     # image=IMAGE_SINGUP
                                     )
        button_singup.grid(pady=10, row=3, column=0, padx=5)

        button_delete = tk.CTkButton(frame_teste, text='Deletar Produto', font=b_font,
                                     # command=lambda: ScreenClient.validation_delete(master),
                                     # image=IMAGE_DELETE
                                     )
        button_delete.grid(pady=10, row=3, column=1, padx=5)

        button_alterar = tk.CTkButton(frame_teste, text='Alterar Produto', font=b_font,
                                      # command=lambda: ScreenClient.validation_alteration(master),
                                      # image=IMAGE_ALTERAR
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
            global client_id

            item_selecionado = table.selection()[0]
            client_id = int(table.item(item_selecionado, 'values')[0])

        table.bind("<<TreeviewSelect>>", get_dados)

    # def show_context_menu(self, event):
    #     menu = Menu(self, tearoff=0, bg="#1f1f1f", fg="#B0C4DE")
    #     menu.add_command(label='Editar', command=lambda: self.validation_alteration(self.master))
    #     menu.add_command(label='Deletar', command=lambda: self.validation_delete(self.master))
    #     menu.tk_popup(event.x_root, event.y_root)
    #
    # @staticmethod
    # def validation_alteration(master):
    #     global client_id
    #     if client_id == 0:
    #         messagebox.showinfo('Info', 'Selecione um cliente!')
    #     else:
    #         master.show_frame(AlterationClientScreen)
    #
    # @staticmethod
    # def validation_delete(master):
    #     global client_id
    #     if client_id == 0:
    #         messagebox.showinfo('Info', 'Selecione um cliente!')
    #     else:
    #         master.show_frame(DeleteClientScreen)
