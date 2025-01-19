import customtkinter as tk
from src.interface._clients import ScreenClient


class SingUpScreen(tk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        label = tk.CTkLabel(self, text='Cadastro')
        label.pack(pady=10, padx=10)

        button = tk.CTkButton(self, text='Clique aqui', command=lambda: master.show_frame(ScreenClient))
        button.pack(pady=10, padx=10)


class LoginScreen(tk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        font_title = tk.CTkFont(weight='bold', size=20, family='Arial')

        label = tk.CTkLabel(self, text='Login', font=font_title)
        label.grid(row=0, column=0, pady=10, sticky='w')
