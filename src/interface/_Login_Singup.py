import tkinter as tk
from src.interface._clients import ScreenClient


class SingUpScreen(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        label = tk.Label(self, text='Cadastro', font=30)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text='Clique aqui',
                           command=lambda: master.show_frame(ScreenClient))
        button.pack(pady=10, padx=10)


class LoginScreen(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        font_title = tk.font.Font(weight='bold', size=20, family='Arial')

        label = tk.Label(self, text='Login', font=font_title)
        label.grid(row=0, column=0, pady=10, sticky='w')


