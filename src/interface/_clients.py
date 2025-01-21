import json
from src._client import Client
import customtkinter as tk
from tkinter import messagebox
from tkinter import ttk
from json import loads
from src._functions import format_adress, get_cep_infos, fonts

client_id = 0


class ScreenClient(tk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color='#1f1f1f')

        b_font, t_font, f_font = fonts()

        texto = tk.CTkLabel(self, text='Clientes cadastrados:', font=t_font)
        texto.pack(pady=10, anchor='w')

        table = ttk.Treeview(self, columns=("id", "Nome", "Email", "CEP", "Rua"), show="headings")

        table.heading("id", text="ID")
        table.heading("Nome", text="Nome")
        table.heading("Email", text="Email")
        table.heading("CEP", text="CEP")
        table.heading("Rua", text="Rua")

        table.column("id", width=50, anchor="center")
        table.column("Nome", width=100, anchor="center")
        table.column("Email", width=150, anchor="center")
        table.column("CEP", width=75, anchor="center")
        table.column("Rua", width=75, anchor="center")

        dados = Client.list_client()

        for cl_id, nome, email, endereco, status in dados:
            endereco = loads(endereco)
            table.insert(
                "", tk.END, values=(
                    cl_id,
                    nome.title(),
                    email.title(),
                    endereco["cep"],
                    f'{endereco["logradouro"].title()} {endereco["numero"]}'
            ))

        table.pack(fill=tk.BOTH, expand=True)

        frame_teste = tk.CTkFrame(self, fg_color='#1f1f1f')
        frame_teste.pack(pady=10)

        button_singup = tk.CTkButton(frame_teste, text='Cadastrar Cliente', font=b_font,
                                  command=lambda: master.show_frame(RegisterClientScreen))
        button_singup.grid(pady=10, row=3, column=0, padx=5)

        button_delete = tk.CTkButton(frame_teste, text='Deletar Cliente', font=b_font,
                                  command=lambda: ScreenClient.validation_delete(master))
        button_delete.grid(pady=10, row=3, column=1, padx=5)

        button_alterar = tk.CTkButton(frame_teste, text='Alterar Cadastro', font=b_font,
                                   command=lambda: ScreenClient.validation_alteration(master))
        button_alterar.grid(pady=10, row=3, column=2, padx=5)

        button_back = tk.CTkButton(frame_teste, text='Voltar', font=b_font,
                                command=lambda: master.initial_frame())
        button_back.grid(pady=10, row=3, column=3, padx=5)

        # button_info = master.get_button_info()
        # button_info.config(command=messagebox.showinfo('Teste1', 'Teste1 aaaaaaa'))

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


class RegisterClientScreen(tk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        b_font, t_font, f_font = fonts()

        text_principal = tk.CTkLabel(self, text='Cadastro de Cliente!', font=t_font)
        text_principal.grid(row=0, column=0, columnspan=9, pady=15)

        label_client_name = tk.CTkLabel(self, text='Nome:')
        label_client_name.grid(row=1, column=0, columnspan=1, sticky='w')

        entry_client_name = tk.CTkEntry(self, width=290)
        entry_client_name.grid(row=2, column=0, columnspan=4, pady=5, sticky='w')

        label_client_email = tk.CTkLabel(self, text='Email:')
        label_client_email.grid(row=3, column=0, pady=5, columnspan=1, sticky='w')

        entry_client_email = tk.CTkEntry(self, width=290)
        entry_client_email.grid(row=4, column=0, pady=5, sticky='w', columnspan=4)

        label_client_cep = tk.CTkLabel(self, text='CEP:')
        label_client_cep.grid(row=5, column=0, pady=5, sticky='w')

        entry_client_cep = tk.CTkEntry(self)
        entry_client_cep.grid(row=6, column=0, pady=5, sticky='w')

        label_client_num = tk.CTkLabel(self, text='Numero:')
        label_client_num.grid(row=5, column=1, pady=5, sticky='w', padx=5)

        entry_client_num = tk.CTkEntry(self)
        entry_client_num.grid(row=6, column=1, pady=5, padx=5)

        button_send = tk.CTkButton(self, text='Enviar', font=b_font,
                                   command=lambda: get_dados(
                                    name=entry_client_name.get(),
                                    email=entry_client_email.get(),
                                    cep=entry_client_cep.get(),
                                    numero=entry_client_num.get(),
                                    master=master
                                    ))
        button_send.grid(row=99, column=0, pady=15)

        button = tk.CTkButton(self, text='Voltar', font=b_font,
                              command=lambda: master.show_frame(ScreenClient))
        button.grid(row=99, column=1, pady=15)

        def get_dados(name, email, cep, numero, master):
            if name == '' or email == '' or numero == '' or cep == '':
                messagebox.showinfo('Info', 'Preencha todos os campos')
                return None

            endereco_incompleto = get_cep_infos(cep)
            if endereco_incompleto != 'CEP invalido!':
                adress = format_adress(endereco_incompleto, numero)
                try:
                    cl = Client(name, email, adress)
                except ValueError as err:
                    messagebox.showerror('Info', message=str(err))
                else:
                    cl.insert_client()
                    cl = None
                    messagebox.showinfo('Info', message='Cliente cadastrado com Sucesso!')
                    master.show_frame(ScreenClient)
            else:
                messagebox.showerror('Info', message=endereco_incompleto)


class AlterationClientScreen(tk.CTkFrame):
    
    def __init__(self, master):
        super().__init__(master)

        global client_id

        b_font, t_font, f_font = fonts()

        client_dados = list(Client.search_client(client_id, dados=True))[0]
        client_dados = Client(client_dados[0], client_dados[1], json.loads(client_dados[2]))

        text_principal = tk.CTkLabel(self, text='Alteração de cadastro!', font=tk.CTkFont('Arial', 20, 'bold'))
        text_principal.grid(row=0, column=0, columnspan=9, pady=15)

        label_client_name = tk.CTkLabel(self, text=f'Nome atual: {client_dados.name}', font=f_font)
        label_client_name.grid(row=1, column=0, columnspan=2, sticky='w', pady=10)

        entry_client_name = tk.CTkEntry(self, width=290)
        entry_client_name.grid(row=2, column=0, columnspan=2, pady=5, sticky='w')

        label_client_email = tk.CTkLabel(self, text=f'Email atual: {client_dados.get_email}', font=f_font)
        label_client_email.grid(row=3, column=0, pady=10, columnspan=2, sticky='w',)

        entry_client_email = tk.CTkEntry(self, width=290)
        entry_client_email.grid(row=4, column=0, pady=5, sticky='w', columnspan=2)

        label_client_cep = tk.CTkLabel(self, text=f'CEP atual: {client_dados.get_endereco['cep']}', font=f_font)
        label_client_cep.grid(row=5, column=0, pady=10, sticky='w')

        entry_client_cep = tk.CTkEntry(self)
        entry_client_cep.grid(row=6, column=0, pady=5, sticky='w')

        label_client_num = tk.CTkLabel(self, text=f'Numero atual: {client_dados.get_endereco['numero']}', font=f_font)
        label_client_num.grid(row=5, column=1, pady=10, sticky='w', padx=5)

        entry_client_num = tk.CTkEntry(self)
        entry_client_num.grid(row=6, column=1, pady=5, padx=5)

        button_send = tk.CTkButton(self, text='Alterar', font=b_font,
                                command=lambda: change_user(
                                    master,
                                    entry_client_name.get(),
                                    entry_client_email.get(),
                                    entry_client_cep.get(),
                                    entry_client_num.get()
                                ))
        button_send.grid(row=99, column=0, pady=15)

        button = tk.CTkButton(self, text='Voltar', font=b_font,
                           command=lambda: back_screen(master))
        button.grid(row=99, column=1, pady=15)

        button_info = master.get_button_info()

        button_info.configure(command=lambda: messagebox.showinfo('Teste', 'Teste'))

        def change_user(master, new_name, new_email, new_cep, new_num):
            global client_id

            if new_name == '' and new_email == '' and new_cep == '' and new_num == '':
                messagebox.showinfo('Info', 'Nenhum campo preenchido!')
                return None
            if new_cep != '' and new_num == '':
                messagebox.showinfo('Info', 'Para atualizar o Cep digite o numero')
                return None
            if new_cep == '' and new_num != '':
                messagebox.showinfo('Info', 'Para atualizar o numero digite o cep')
                return None

            new_name = new_name if new_name != '' else None
            new_email = new_email if new_email != '' else None
            new_adress = None

            if new_cep != '' and new_num != '':
                try:
                    new_adress = format_adress(get_cep_infos(new_cep), new_num)
                except ValueError:
                    new_adress = None

            msg = Client.edit_client(client_id, new_name, new_email, new_adress)
            messagebox.showinfo('Info', msg)
            client_id = 0
            master.show_frame(ScreenClient)

        def back_screen(master):
            global client_id
            client_id = 0
            master.show_frame(ScreenClient)


class DeleteClientScreen(tk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        b_font, t_font, f_font = fonts()

        global client_id
        name_client = Client.search_client(client_id)

        label = tk.CTkLabel(self, text=f'Tem certeza que deseja deletar o cliente "{name_client}"?')
        label.grid(row=0, column=0, columnspan=2, pady=15)

        button_yes = tk.CTkButton(self, text='Sim', font=b_font,
                               command=lambda: delete_client(client_id, master))
        button_yes.grid(row=1, column=0)

        button_no = tk.CTkButton(self, text='Não', font=b_font,
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


if __name__ == '__main__':
    pass
