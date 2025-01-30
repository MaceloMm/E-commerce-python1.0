import customtkinter as tk
from tkinter import ttk
from src.interface._Login_Singup import SingUpScreen, LoginScreen
from src._functions import fonts, format_static_path
from src.interface._gerencial import GeneralScreen
import webbrowser
from PIL import Image
from src.interface._orders import OrderScreen


class Application(tk.CTk):

    def __init__(self):
        super().__init__(fg_color='#1f1f1f')

        self.title('Onyx Soluctions Store')
        self.geometry('700x500')
        self.resizable(False, False)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#1f1f1f",
                        foreground="#F0F8FF",
                        fieldbackground="#1f1f1f",
                        rowheight=25,
                        bordercolor="#2b2b2b",
                        borderwidth=2,
                        font=('Calibri', 9),
                        )
        style.map("Treeview",
                  background=[("selected", "#B0C4DE")],
                  foreground=[("selected", "#2b2b2b")],
                  )

        # Configurar os headers
        style.configure("Treeview.Heading",
                        background="#1f1f1f",
                        foreground="#B0C4DE",
                        font=("Arial", 12, "bold"),
                        borderwidth=0)

        style.map("Treeview.Heading",
                  background=[("selected", "#B0C4DE")],
                  foreground=[("selected", "#2b2b2b")]
                  )

        self.current_frame = None

        self.show_frame(FirstScreen)

        b_font, f_font, t_font = fonts()

        self.name_store = tk.CTkLabel(self, text='Onyx Store',
                                      font=tk.CTkFont(weight='bold', size=30, family='Helvetica'))
        self.name_store.place(x=25, y=15, anchor='nw')

        self.button_teste = tk.CTkButton(self, text='¡', width=2, font=b_font)
        self.button_teste.place(x=685, y=485, anchor='se')

    def show_frame(self, frame_class):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame_class(self)
        self.current_frame.configure(fg_color='#1f1f1f')
        self.current_frame.place(relx=0.5, rely=0.5, anchor="center")

    def initial_frame(self):
        Application.show_frame(self, FirstScreen)

    def get_button_info(self):
        return self.button_teste

    @staticmethod
    def get_gerencial_screen():
        return GeneralScreen


class FirstScreen(tk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, width=700, height=300)
        self.configure(fg_color='#1f1f1f')
        self.grid_propagate(False)

        self.rowconfigure([0, 1, 2, 3, 4], weight=1)
        self.columnconfigure(0, weight=1)

        b_font, t_font, f_font = fonts()

        principal_text = tk.CTkLabel(self, text='Escolha uma das opções:', font=t_font)
        principal_text.grid(row=0, column=0, pady=10)

        image_login = tk.CTkImage(dark_image=Image.open(format_static_path('icon', 'user.png')).resize((15, 15)),
                                  light_image=Image.open(format_static_path('icon', 'user.png')).resize((15, 15)),
                                  size=(15, 15))

        image_singup = tk.CTkImage(dark_image=Image.open(format_static_path('icon', 'add-user.png')).resize((15, 15)),
                                   light_image=Image.open(format_static_path('icon', 'add-user.png')).resize((15, 15)),
                                   size=(15, 15)
                                   )

        image_help = tk.CTkImage(dark_image=Image.open(format_static_path('icon', 'help.png')).resize((15, 15)),
                                 light_image=Image.open(format_static_path('icon', 'help.png')).resize((15, 15)),
                                 size=(15, 15)
                                 )

        image_exit = tk.CTkImage(dark_image=Image.open(format_static_path('icon', 'logout.png')).resize((25, 25)),
                                 light_image=Image.open(format_static_path('icon', 'logout.png')).resize((25, 25)),
                                 size=(15, 15))

        button_login = tk.CTkButton(self, text='Login', font=b_font, width=200, height=30,
                                    command=lambda: Application.show_frame(master, LoginScreen),
                                    image=image_login, compound='left', anchor='center')
        button_login.grid(row=1, column=0, pady=5)

        button_singup = tk.CTkButton(self, text='Cadastro', font=b_font, width=200, height=30,
                                     command=lambda: Application.show_frame(master, SingUpScreen),
                                     image=image_singup)
        button_singup.grid(row=2, column=0, pady=5)

        help_button = tk.CTkButton(self, text='Ajuda', font=b_font, width=200, height=30,
                                   command=lambda: webbrowser.open('https://github.com/MaceloMm'),
                                   image=image_help)
        help_button.grid(row=3, column=0, pady=5)

        exit_button = tk.CTkButton(self, text='Sair', font=b_font, width=200, height=30,
                                   command=lambda: exit_application(master),
                                   image=image_exit)
        exit_button.grid(row=4, column=0, pady=5)

        def exit_application(app):
            app.quit()
            exit(1)


root = Application()


if __name__ == '__main__':
    root = Application()
    root.mainloop()
