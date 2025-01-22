import customtkinter as tk


class OrderScreen(tk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        label = tk.CTkLabel(self, text='Teste')