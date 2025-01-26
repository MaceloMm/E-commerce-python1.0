import customtkinter as tk
from src.interface._clients import ScreenClient
from src._functions import fonts
from src.interface._products import ScreenProduct
from src.interface._imagens import IMAGE_BACK, IMAGE_ORDER, IMAGE_PRODUCT, IMAGE_GERENCIAL


class GeneralScreen(tk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        b_font, t_font, f_font = fonts()

        principal_text = tk.CTkLabel(self, text='Menu gerencial', font=t_font)
        principal_text.grid(pady=10, column=0, row=0)

        button_client = tk.CTkButton(self, text='Gerenciar de Clientes', font=b_font, width=250, height=30,
                                     command=lambda: master.show_frame(ScreenClient), image=IMAGE_GERENCIAL)
        button_client.grid(pady=15, column=0, row=1)

        button_products = tk.CTkButton(self, text='Gerenciar de Produtos', font=b_font, width=250, height=30,
                                       command=lambda: master.show_frame(ScreenProduct), image=IMAGE_PRODUCT)
        button_products.grid(pady=15, column=0, row=2)

        button_order = tk.CTkButton(self, text='Realizar pedidos', font=b_font, width=250, height=30, image=IMAGE_ORDER)
        button_order.grid(pady=15, column=0, row=3)

        button_back = tk.CTkButton(self, text='Voltar', font=b_font, width=250, height=30,
                                   command=lambda: master.initial_frame(), image=IMAGE_BACK)
        button_back.grid(pady=15, column=0, row=4)
