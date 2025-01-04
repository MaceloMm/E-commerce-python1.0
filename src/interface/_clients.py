import tkinter as tk
from src._client import Client


class ScreenClient(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        texto = tk.Label(self, text='Clientes')
        texto.grid(pady=10, row=0, column=0)

        button_singup = tk.Button(self, text='Cadastrar Cliente', font=12, command=lambda x: x)
        button_singup.grid(pady=10, row=1, column=0)

        button_delete = tk.Button(self, text='Deletar Cliente', font=12, command=lambda x: x)
        button_delete.grid(pady=10, row=2, column=0)

        button_alterar = tk.Button(self, text='Alterar Cadastro', font=12, command=lambda x: x)
        button_alterar.grid(pady=10, row=3, column=0)

        button_back = tk.Button(self, text='Voltar', font=12, command=lambda: master.show_frame())
        button_back.grid(pady=10, row=4, column=0)

