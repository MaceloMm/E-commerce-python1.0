from src._client import Client
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from json import loads
from src._functions import format_adress

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

        for cl_id, nome, email, endereco, status in dados:
            endereco = loads(endereco)
            table.insert(
                "", tk.END, values=(
                    cl_id,
                    nome.title(),
                    email.title(),
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

        textprincipal = tk.Label(self, text='Cadastro de Cliente!')
        textprincipal.grid(row=0, column=0, columnspan=6)

        label_client_name = tk.Label(self, text='Nome:')
        label_client_name.grid(row=1, column=0)

        entry_client_name = tk.Entry(self)
        entry_client_name.grid(row=1, column=1)

        label_client_email = tk.Label(self, text='Email:')
        label_client_email.grid(row=2, column=0)

        entry_client_email = tk.Entry(self)
        entry_client_email.grid(row=2, column=1)

        label_client_cep = tk.Label(self, text='CEP:')
        label_client_cep.grid(row=3, column=0)

        entry_client_cep = tk.Entry(self,)
        entry_client_cep.grid(row=3, column=1)

        label_client_rua = tk.Label(self, text='Rua:')
        label_client_rua.grid(row=3, column=2)

        entry_client_rua = tk.Entry(self)
        entry_client_rua.grid(row=3, column=3)

        label_client_num = tk.Label(self, text='Numero:')
        label_client_num.grid(row=3, column=4)

        entry_client_num = tk.Entry(self)
        entry_client_num.grid(row=3, column=5)

        button_send = tk.Button(self, text='Enviar',
                                command=lambda: get_dados(
                                    name=entry_client_name.get(),
                                    email=entry_client_email.get(),
                                    adress=format_adress(
                                        cep=entry_client_cep.get(),
                                        rua=entry_client_rua.get(),
                                        num=int(entry_client_num.get())
                                    )))
        button_send.grid(row=99, column=0, pady=10)

        button = tk.Button(self, text='Voltar', command=lambda: master.show_frame(ScreenClient))
        button.grid(row=99, column=1, pady=10)

        def get_dados(name, email, adress):
            cl = Client(name, email, adress)
            cl.insert_client()
            cl = None
            print('Cliente cadastrado!')


class AlterationClientScreen(tk.Frame):
    
    def __init__(self, master):
        super().__init__(master)

        global client_id

        buttons_fonts = tk.font.Font(size=11, weight='bold')
        title_font = tk.font.Font(size=14, weight='bold')

        client_dados = list(Client.search_client(client_id, dados=True))[0]
        client_dados = Client(client_dados[0], client_dados[1], client_dados[2])

        button_no = tk.Button(self, text='Não', width=15, height=1, font=buttons_fonts,
                              command=lambda: back_screen(master))
        button_no.grid(row=1, column=1)

        def back_screen(master):
            global client_id
            client_id = 0
            master.show_frame(ScreenClient)


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
                              command=lambda: back_screen(master))
        button_no.grid(row=1, column=1)

        def delete_client(c_id, master):
            global client_id
            msg = Client.delete_client(c_id)
            messagebox.showinfo('Info', message=msg)
            client_id = 0
            master.show_frame(ScreenClient)

        def back_screen(master):
            global client_id
            client_id = 0
            master.show_frame(ScreenClient)


