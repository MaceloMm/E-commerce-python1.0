from src._client import Client
import tkinter as tk
from tkinter import ttk
from json import loads


class ScreenClient(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        buttons_fonts = tk.font.Font(size=11, weight='bold')
        title_font = tk.font.Font(size=14, weight='bold')

        texto = tk.Label(self, text='Clientes cadastrados:', font=title_font)
        texto.grid(pady=10, row=0, column=0, columnspan=4, sticky='w')

        button_singup = tk.Button(self, text='Cadastrar Cliente', font=buttons_fonts, width=15, height=1,
                                  command=lambda x: x)
        button_singup.grid(pady=10, row=3, column=0, padx=5)

        button_delete = tk.Button(self, text='Deletar Cliente', font=buttons_fonts, width=15, height=1,
                                  command=lambda x: x)
        button_delete.grid(pady=10, row=3, column=1, padx=5)

        button_alterar = tk.Button(self, text='Alterar Cadastro', font=buttons_fonts, width=15, height=1,
                                   command=lambda x: x)
        button_alterar.grid(pady=10, row=3, column=2, padx=5)

        button_back = tk.Button(self, text='Voltar', font=buttons_fonts, width=15, height=1,
                                command=lambda: master.initial_frame())
        button_back.grid(pady=10, row=3, column=3, padx=5)

        table = ttk.Treeview(self, columns=("id", "Nome", "Email", "Coluna 4"), show="headings")

        table.heading("id", text="ID")
        table.heading("Nome", text="Nome")
        table.heading("Email", text="Email")
        table.heading("Coluna 4", text="Endereço")

        table.column("id", width=45, anchor="center")
        table.column("Nome", width=100, anchor="center")
        table.column("Nome", width=155, anchor="center")
        table.column("Coluna 4", width=200, anchor="center")

        dados = Client.list_client()

        for id, nome, email, endereco in dados:
            endereco = loads(endereco)
            table.insert("", tk.END, values=(id, nome, email, endereco["bairro"]))

        table.grid(row=2, column=0, columnspan=4)





