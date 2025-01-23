import customtkinter as tk


class OrderScreen(tk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        label = tk.CTkLabel(self, text='Teste')
        label.pack(pady=10, padx=10)

