import customtkinter as tk
from src.interface._clients import ScreenClient
from src._functions import fonts
from src.interface._products import ScreenProduct


class GeneralScreen(tk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        b_font, t_font, f_font = fonts()

        principal_text = tk.CTkLabel(self, text='Menu gerencial', font=t_font)
        principal_text.grid(pady=10, column=0, row=0)

        button_client = tk.CTkButton(self, text='Gerenciamento de Clientes', font=b_font, width=250,
                                     command=lambda: master.show_frame(ScreenClient))
        button_client.grid(pady=15, column=0, row=1)

        button_products = tk.CTkButton(self, text='Gerenciamento de Produtos', font=b_font, width=250,
                                       command=lambda: master.show_frame(ScreenProduct))
        button_products.grid(pady=15, column=0, row=2)

        button_order = tk.CTkButton(self, text='Realizar pedidos', font=b_font, width=250)
        button_order.grid(pady=15, column=0, row=3)

        button_back = tk.CTkButton(self, text='Voltar', font=b_font, width=250,
                                   command=lambda: master.initial_frame())
        button_back.grid(pady=15, column=0, row=4)
