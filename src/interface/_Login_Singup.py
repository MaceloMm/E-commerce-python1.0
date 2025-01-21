import customtkinter as tk
from src.interface._clients import ScreenClient
from src._functions import fonts
from tkinter import messagebox
from typing import Union
from src._users import User


class SingUpScreen(tk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        b_font, t_font, f_font = fonts()

        principal_text = tk.CTkLabel(self, text='Cadastro!', font=t_font)
        principal_text.grid(pady=10, column=0, columnspan=2, row=0)

        email_label = tk.CTkLabel(self, text='Email:', font=f_font)
        email_label.grid(pady=3, column=0, row=1, sticky='nw', columnspan=2)

        email_entry = tk.CTkEntry(self, width=300, placeholder_text='Email')
        email_entry.grid(column=0, row=2, columnspan=2)

        password_label = tk.CTkLabel(self, text='Senha:', font=f_font)
        password_label.grid(pady=3, column=0, row=3, sticky='nw', columnspan=2)

        password_entry = tk.CTkEntry(self, width=300, placeholder_text='Senha', show='*')
        password_entry.grid(column=0, row=4, columnspan=2)

        password_confirm_label = tk.CTkLabel(self, text='Confirma senha:', font=f_font)
        password_confirm_label.grid(column=0, row=5, columnspan=2, sticky='nw')

        password_confirm_entry = tk.CTkEntry(self, width=300, placeholder_text='Confirma Senha', show='*')
        password_confirm_entry.grid(column=0, row=6, columnspan=2)

        button_send = tk.CTkButton(self, text='Cadastrar', font=b_font,
                                   command=lambda: SingUpScreen.create_user(
                                       master=master, email=email_entry.get(), password=password_entry.get(),
                                       confirm_password=password_confirm_entry.get()
                                   ))
        button_send.grid(column=0, row=7, pady=20)

        button_back = tk.CTkButton(self, text='Voltar', font=b_font,
                                   command=lambda: master.initial_frame())
        button_back.grid(column=1, row=7, pady=20)

    @staticmethod
    def create_user(master, email, password, confirm_password) -> Union[str, None]:
        if email == '' and password == '' and confirm_password == '':
            messagebox.showerror('Info', 'Nenhum campo preenchido!')
            return None
        if password != confirm_password:
            messagebox.showerror('Info', 'Senhas não estão iguais!')
            return None

        try:
            u = User(email, password)
        except ValueError as err:
            messagebox.showerror('Info', str(err))
        else:
            ret = u.insert_user()
            if ret != 'Usuário cadastrado com sucesso!':
                messagebox.showerror('Info', ret)
                return None
            messagebox.showinfo('Info', ret)
            master.initial_frame()



class LoginScreen(tk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        font_title = tk.CTkFont(weight='bold', size=20, family='Arial')

        label = tk.CTkLabel(self, text='Login', font=font_title, cursor="hand2")
        label.pack(pady=10, padx=10)

        label.bind("<Button-1>", self.teste)

        button = tk.CTkButton(self, text='Clique aqui', fg_color=None, hover_color=None, command=lambda: master.show_frame(ScreenClient))
        button.pack(pady=10, padx=10)

    def teste(self, event):
        print('teste')
