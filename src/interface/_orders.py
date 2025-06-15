import customtkinter as tk
from typing import Union, Callable
from src.models._product import Product
from src.models._client import Client
from src.interface._imagens import IMAGE_BACK
from src._functions import fonts


class FloatSpinbox(tk.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = tk.CTkButton(self, text="-", width=height - 6, height=height - 6,
                                            command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = tk.CTkEntry(self, width=width - (2 * height), height=height - 6, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = tk.CTkButton(self, text="+", width=height - 6, height=height - 6,
                                       command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, "0.0")

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) + self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) - self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> Union[float, None]:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(float(value)))


class ScrollabFrameProduct(tk.CTkScrollableFrame):
    checkboxes = []

    def __init__(self, master, title, values, largura, altura, color='#1f1f1f'):
        b_font, t_font, f_font = fonts()
        super().__init__(master, label_text=title, width=largura, height=altura, fg_color=color,
                         label_font=f_font)
        self.grid_columnconfigure(0, weight=1)
        self.values = values

        for i, value in enumerate(self.values):
            checkbox = tk.CTkCheckBox(self, text=value, font=f_font)
            checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            t = FloatSpinbox(self, step_size=1, width=100, height=25)
            t.grid(row=i, column=1, sticky="e", pady=(10, 0))

            ScrollabFrameProduct.checkboxes.append((checkbox, t))

    @classmethod
    def get(cls):
        checked_checkboxes = []
        for checkbox, t in cls.checkboxes:
            if checkbox.get() == 1 and t.get() > 0:
                checked_checkboxes.append((checkbox.cget("text"), int(t.get())))
        return checked_checkboxes


class ScrollabFrameClients(tk.CTkScrollableFrame):
    radio = []

    def __init__(self, master, title, values, largura, altura, color='#1f1f1f'):
        b_font, t_font, f_font = fonts()
        super().__init__(master, label_text=title, width=largura, height=altura, fg_color=color,
                         label_font=f_font)
        self.grid_columnconfigure(0, weight=1)
        self.values = values

        self.radio_var = tk.StringVar(value="")

        for i, value in enumerate(self.values):
            radio = tk.CTkRadioButton(self, text=value, variable=self.radio_var, value=str(value), font=f_font)
            radio.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")

    def get(self):
        return self.radio_var.get()


class ButtonsFrame(tk.CTkFrame):

    def __init__(self, master, width=200, height=200, color='#1f1f1f', true_master=None):

        b_font, t_font, f_font = fonts()

        super().__init__(master, width=width, height=height, fg_color=color)

        buttons_enviar = tk.CTkButton(self, text='Enviar', font=b_font, command=lambda: print())
        buttons_enviar.grid(pady=10, padx=10, column=0, row=0)

        button_cart = tk.CTkButton(self, text='Carrinho', font=b_font)
        button_cart.grid(pady=10, padx=10, column=1, row=0)

        button_consult = tk.CTkButton(self, text='Pedidos', font=b_font)
        button_consult.grid(pady=10, padx=10, column=2, row=0)

        buttons_back = tk.CTkButton(self, text='Voltar', image=IMAGE_BACK, font=b_font,
                                    command=lambda: true_master.initial_frame())
        buttons_back.grid(pady=10, padx=10, column=3, row=0)


class OrderScreen(tk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        produts_names = Product.list_product(seach_name=True)
        client_names = Client.list_client(search_name=True)

        produts_view = ScrollabFrameProduct(self, title='Produtos', values=produts_names, largura=400, altura=230)
        produts_view.grid(column=0, row=0, padx=10)

        client_views = ScrollabFrameClients(self, title='Clientes', values=client_names, largura=200, altura=230)
        client_views.grid(column=1, row=0, padx=10)

        buttons_views = ButtonsFrame(self, width=600, height=200, true_master=master)
        buttons_views.grid(column=0, row=1, pady=20, columnspan=2)



