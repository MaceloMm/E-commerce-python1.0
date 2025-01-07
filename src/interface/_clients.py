from src._client import Client
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from json import loads

client_id = 0


class ScreenClient(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        buttons_fonts = tk.font.Font(size=11, weight='bold')
        title_font = tk.font.Font(size=14, weight='bold')

        texto = tk.Label(self, text='Clientes cadastrados:', font=title_font)
        texto.pack(pady=10, anchor='w')
        # texto.grid(pady=10, row=0, column=0, columnspan=4, sticky='w')

        table = ttk.Treeview(self, columns=("id", "Nome", "Email", "CEP", "Rua"), show="headings")

        table.heading("id", text="ID")
        table.heading("Nome", text="Nome")
        table.heading("Email", text="Email")
        table.heading("CEP", text="CEP")
        table.heading("Rua", text="Rua")

        table.column("id", width=45, anchor="center")
        table.column("Nome", width=75, anchor="center")
        table.column("Email", width=120, anchor="center")
        table.column("CEP", width=50, anchor="center")
        table.column("Rua", width=50, anchor="center")

        dados = Client.list_client()

        for id, nome, email, endereco in dados:
            endereco = loads(endereco)
            table.insert(
                "", tk.END, values=(
                    id,
                    nome,
                    email,
                    endereco["CEP"],
                    f'{endereco["Rua"].title()} {endereco["Numero"]}'
            ))

        table.pack(fill=tk.BOTH, expand=True)

        frame_teste = tk.Frame(self)
        frame_teste.pack(pady=10)

        button_singup = tk.Button(frame_teste, text='Cadastrar Cliente', font=buttons_fonts, width=15, height=1,
                                  command=lambda: master.show_frame(RegisterClientScreen))
        button_singup.grid(pady=10, row=3, column=0, padx=5)

        button_delete = tk.Button(frame_teste, text='Deletar Cliente', font=buttons_fonts, width=15, height=1,
                                  command=lambda: ScreenClient.validation_delete(master))
        button_delete.grid(pady=10, row=3, column=1, padx=5)

        button_alterar = tk.Button(frame_teste, text='Alterar Cadastro', font=buttons_fonts, width=15, height=1,
                                   command=lambda: ScreenClient.validation_alteration(master))
        button_alterar.grid(pady=10, row=3, column=2, padx=5)

        button_back = tk.Button(frame_teste, text='Voltar', font=buttons_fonts, width=15, height=1,
                                command=lambda: master.initial_frame())
        button_back.grid(pady=10, row=3, column=3, padx=5)

        def get_dados(event):
            global client_id

            item_selecionado = table.selection()[0]
            client_id = int(table.item(item_selecionado, 'values')[0])

        table.bind("<<TreeviewSelect>>", get_dados)

    @staticmethod
    def validation_alteration(master):
        global client_id
        if client_id == 0:
            messagebox.showinfo('Info', 'Selecione um cliente!')
        else:
            master.show_frame(AlterationClientScreen)

    @staticmethod
    def validation_delete(master):
        global client_id
        if client_id == 0:
            messagebox.showinfo('Info', 'Selecione um cliente!')
        else:
            master.show_frame(DeleteClientScreen)


class RegisterClientScreen(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        button = tk.Button(self, text='Voltar', command=lambda: master.show_frame(ScreenClient))
        button.pack(pady=10)


class AlterationClientScreen(tk.Frame):
    
    def __init__(self, master):
        super().__init__(master)

        global client_id

        print(client_id)

        button = tk.Button(self, text='Voltar', command=lambda: master.show_frame(ScreenClient))
        button.pack(pady=10)


class DeleteClientScreen(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        buttons_fonts = tk.font.Font(size=11, weight='bold')
        title_font = tk.font.Font(size=14, weight='bold')

        global client_id
        name_client = Client.search_client(client_id)

        label = tk.Label(self, text=f'Tem certeza que deseja deletar o cliente "{name_client}"?')
        label.grid(row=0, column=0, columnspan=2)

        button_yes = tk.Button(self, text='Sim', width=15, height=1, font=buttons_fonts,
                               command=lambda: delete_client(client_id, master))
        button_yes.grid(row=1, column=0)

        button_no = tk.Button(self, text='Não', width=15, height=1, font=buttons_fonts,
                              command=lambda: master.show_frame(ScreenClient))
        button_no.grid(row=1, column=1)

        def delete_client(c_id, master):
            global client_id
            msg = Client.delete_client(c_id)
            messagebox.showinfo('Info', message=msg)
            client_id = 0
            master.show_frame(ScreenClient)

