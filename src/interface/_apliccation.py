import tkinter as tk
from ttkbootstrap import Style
from _Login_Singup import SingUpScreen, LoginScreen
from src._client import Client


class Application(tk.Tk):

    def __init__(self, master=None):
        super().__init__()

        self.title('Onyx Soluctions Store')
        self.geometry('600x600')

        Style(theme='darkly')

        self.current_frame = None

        self.show_frame(FirstScreen)

    def show_frame(self, frame_class):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame_class(self)
        self.current_frame.place(relx=0.5, rely=0.5, anchor='center')


class FirstScreen(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        principal_text = tk.Label(self, text='Escolha uma das opções:', font=20)
        principal_text.grid(row=0, column=0, pady=10, columnspan=2)

        button_login = tk.Button(self, text='Login', width=12, height=1,
                                 command=lambda: Application.show_frame(master, LoginScreen)
                                 )
        button_login.grid(row=2, column=0, pady=10)

        button_singup = tk.Button(self, text='Cadastro', width=12, height=1,
                                  command=lambda: Application.show_frame(master, SingUpScreen)
                                  )
        button_singup.grid(row=2, column=1, pady=10)


if __name__ == '__main__':
    root = Application()
    root.mainloop()

