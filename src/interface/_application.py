import tkinter as tk
from ttkbootstrap import Style
from src.interface._Login_Singup import SingUpScreen, LoginScreen
from src._functions import fonts


class Application(tk.Tk):

    def __init__(self, master=None):
        super().__init__()

        self.title('Onyx Soluctions Store')
        self.geometry('700x500')
        self.maxsize(width=700, height=500)
        self.minsize(width=700, height=500)

        Style(theme='cyborg')
        #Style(theme='darkly')

        self.current_frame = None

        self.show_frame(FirstScreen)

        b_font, f_font = fonts()

        self.button_teste = tk.Button(self, text='¡', width=2, font=b_font)
        self.button_teste.place(x=685, y=485, anchor='se')

    def show_frame(self, frame_class):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame_class(self)
        self.current_frame.place(relx=0.5, rely=0.5, anchor='center')

    def initial_frame(self):
        Application.show_frame(self, FirstScreen)

    def get_button_info(self):
        return self.button_teste


class FirstScreen(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        b_font, t_font = fonts()

        principal_text = tk.Label(self, text='Escolha uma das opções:', font=t_font)
        principal_text.grid(row=0, column=0, pady=10, columnspan=2)

        button_login = tk.Button(self, text='Login', width=12, height=1, font=b_font,
                                 command=lambda: Application.show_frame(master, LoginScreen)
                                 )
        button_login.grid(row=2, column=0, pady=10)

        button_singup = tk.Button(self, text='Cadastro', width=12, height=1, font=b_font,
                                  command=lambda: Application.show_frame(master, SingUpScreen)
                                  )
        button_singup.grid(row=2, column=1, pady=10)


root = Application()


if __name__ == '__main__':
    root = Application()
    root.mainloop()

