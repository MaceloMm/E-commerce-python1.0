import customtkinter as tk
from src._functions import fonts
from tkinter import messagebox
from typing import Union
from src.models._users import User
from src.interface._orders import OrderScreen
from src.interface._gerencial import GeneralScreen
from src.send_email import EmailBackendOnyx
import threading
import queue


code = ''
email_check = ''
password_check = ''


class SingUpScreen(tk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        b_font, t_font, f_font = fonts()

        principal_text = tk.CTkLabel(self, text='Cadastro!', font=t_font)
        principal_text.grid(pady=10, column=0, columnspan=2, row=0)

        email_label = tk.CTkLabel(self, text='Email:', font=f_font)
        email_label.grid(pady=3, column=0, row=1, sticky='nw', columnspan=2)

        self.email_entry = tk.CTkEntry(self, width=300, placeholder_text='Email')
        self.email_entry.grid(column=0, row=2, columnspan=2)

        password_label = tk.CTkLabel(self, text='Senha:', font=f_font)
        password_label.grid(pady=3, column=0, row=3, sticky='nw', columnspan=2)

        self.password_entry = tk.CTkEntry(self, width=300, placeholder_text='Senha', show='*')
        self.password_entry.grid(column=0, row=4, columnspan=2)

        password_confirm_label = tk.CTkLabel(self, text='Confirma senha:', font=f_font)
        password_confirm_label.grid(column=0, row=5, columnspan=2, sticky='nw')

        self.password_confirm_entry = tk.CTkEntry(self, width=300, placeholder_text='Confirma Senha', show='*')
        self.password_confirm_entry.grid(column=0, row=6, columnspan=2)

        button_send = tk.CTkButton(self, text='Cadastrar', font=b_font,
                                   command=lambda: self.create_user(
                                        email=self.email_entry.get(), password=self.password_entry.get(),
                                        confirm_password=self.password_confirm_entry.get()
                                   ))
        button_send.grid(column=0, row=7, pady=20)

        button_back = tk.CTkButton(self, text='Voltar', font=b_font,
                                   command=lambda: master.initial_frame())
        button_back.grid(column=1, row=7, pady=20)

        self.email_entry.bind('<Return>', self.on_press)
        self.password_entry.bind('<Return>', self.on_press)
        self.password_confirm_entry.bind('<Return>', self.on_press)

        self.loadding_label = tk.CTkLabel(self, text='', font=f_font)
        self.loadding_label.grid(column=0, row=8, columnspan=2)

    def on_press(self, event):
        self.create_user(email=self.email_entry.get(), password=self.password_entry.get(),
                         confirm_password=self.password_confirm_entry.get())

    def create_user(self, email, password, confirm_password) -> Union[str, None]:
        global code

        for i in User.list_users():
            if i == email:
                messagebox.showinfo('Info', 'Email já cadastrado!')
                return None

        if email == '' and password == '' and confirm_password == '':
            messagebox.showerror('Info', 'Nenhum campo preenchido!')
            return None
        if password != confirm_password:
            messagebox.showerror('Info', 'Senhas não estão iguais!')
            return None

        def send_email_task(email, result_queue):
            code, ret = EmailBackendOnyx.send_email(email)
            result_queue.put((code, ret))

        def check_queue():
            global code
            global email_check
            global password_check
            if not result_queue.empty():
                code, ret = result_queue.get()
                email_check = email
                password_check = password
                messagebox.showinfo('Info', ret)
                self.master.show_frame(CheckCode)
            else:
                self.master.after(100, check_queue)

        result_queue = queue.Queue()

        self.loadding_label.configure(text="Enviando aguarde...")
        threading.Thread(target=send_email_task, args=(self.email_entry.get(), result_queue)).start()
        check_queue()

        # try:
        #     u = User(email, password)
        # except ValueError as err:
        #     messagebox.showerror('Info', str(err))
        # else:
        #     ret = u.insert_user()
        #     if ret != 'Usuário cadastrado com sucesso!':
        #         messagebox.showerror('Info', ret)
        #         return None
        #     messagebox.showinfo('Info', ret)
        #     master.initial_frame()


class LoginScreen(tk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        b_font, t_font, f_font = fonts()

        principal_text = tk.CTkLabel(self, text='Login', font=t_font)
        principal_text.grid(column=0, row=0, pady=10, columnspan=2)

        self.email_login_label = tk.CTkLabel(self, text='Email:', font=f_font)
        self.email_login_label.grid(column=0, row=1, pady=5, sticky='nw', columnspan=2)

        self.email_login_entry = tk.CTkEntry(self, placeholder_text='Email', width=300)
        self.email_login_entry.grid(column=0, row=2, columnspan=2)

        password_login_label = tk.CTkLabel(self, text='Senha:', font=f_font)
        password_login_label.grid(column=0, row=3, pady=5, sticky='nw', columnspan=2)

        self.password_login_entry = tk.CTkEntry(self, width=300, placeholder_text='Senha', show='*')
        self.password_login_entry.grid(column=0, row=4, columnspan=2)

        self.forget_password = tk.CTkLabel(self, cursor='hand2', text='Esqueceu a senha?', font=("calibri", 14))
        self.forget_password.grid(column=0, row=5, columnspan=2, sticky='nw', pady=2, padx=2)

        self.forget_password.bind("<Enter>", self.on_hover)
        self.forget_password.bind("<Leave>", self.off_hover)
        self.forget_password.bind("<Button-1>", self.on_click)

        button_login = tk.CTkButton(self, text='Login', font=b_font,
                                    command=lambda: LoginScreen.login_checkup(
                                        master, email=self.email_login_entry.get(),
                                        password=self.password_login_entry.get().encode()))
        button_login.grid(column=0, row=6, pady=20, sticky='w')

        self.bind('<Return>', self.on_press)
        self.email_login_entry.bind('<Return>', self.on_press)
        self.password_login_entry.bind('<Return>', self.on_press)

        button_back = tk.CTkButton(self, text='Voltar', font=b_font, command=lambda: master.initial_frame())
        button_back.grid(column=1, row=6, pady=20, sticky='w')

    def on_hover(self, event):
        self.forget_password.configure(text_color="#B0C4DE")

    def off_hover(self, event):
        self.forget_password.configure(text_color="white")

    def on_click(self, event):
        self.master.show_frame(RecoverPassword)

    def on_press(self, event):
        LoginScreen.login_checkup(self.master, self.email_login_entry.get(), self.password_login_entry.get().encode())

    @staticmethod
    def login_checkup(master, email, password):
        st = User.check_password(email, password)
        if not isinstance(st, tuple):
            messagebox.showerror('Info', st)
            return None

        if st[0] and st[1] == 'client':
            master.show_frame(OrderScreen)
        elif st[0] and st[1] == 'gerente':
            master.show_frame(GeneralScreen)

        return None


class RecoverPassword(tk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        b_font, t_font, f_font = fonts()

        principal_text = tk.CTkLabel(self, text='Recuperação de Senha!', font=t_font)
        principal_text.grid(column=0, row=0, columnspan=2)

        email_text = tk.CTkLabel(self, text='Email:', font=f_font)
        email_text.grid(column=0, row=1, sticky='nw', pady=15, columnspan=2)

        self.email_entry = tk.CTkEntry(self, placeholder_text='Email...', font=f_font, width=300)
        self.email_entry.grid(column=0, row=2, pady=2, columnspan=2)
        self.email_entry.bind('<Return>', self.on_press)

        button_enviar = tk.CTkButton(self, text='Enviar', font=b_font,
                                     command=lambda: self.get_email()
                                     )
        button_enviar.grid(column=0, row=3, pady=15)

        button_voltar = tk.CTkButton(self, text='Voltar', font=b_font, command=lambda: master.show_frame(LoginScreen))
        button_voltar.grid(column=1, row=3, pady=15)

        self.loading_label = tk.CTkLabel(self, text='', font=f_font)
        self.loading_label.grid(column=0, row=4, columnspan=2, pady=20)

    def get_email(self) -> None:

        def send_email_task(email, result_queue):
            ret_code, ret = EmailBackendOnyx.send_email(email)
            result_queue.put((ret_code, ret))

        def check_queue():
            global code
            if not result_queue.empty():
                code, ret = result_queue.get()
                messagebox.showinfo('Info', ret)
                self.master.show_frame(CheckCode)
            else:
                self.master.after(100, check_queue)

        global code

        if self.email_entry.get() is None or self.email_entry.get() == '':
            messagebox.showinfo('Info', 'Preencha o campo!')
            return None

        if self.email_entry.get() not in User.list_users():
            messagebox.showinfo('Info', 'Email não cadastrado!')
            return None

        result_queue = queue.Queue()

        self.loading_label.configure(text="Enviando aguarde...")
        threading.Thread(target=send_email_task, args=(self.email_entry.get(), result_queue)).start()
        check_queue()

        # code, ret = EmailBackendOnyx.send_email(self.email_entry.get())
        # messagebox.showinfo('Info', ret)
        # self.master.show_frame(CheckCode)

    def on_press(self, event):
        self.get_email()


class CheckCode(tk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        b_font, t_font, f_font = fonts()

        text_principal = tk.CTkLabel(self, text='Recuperação de senha!', font=t_font)
        text_principal.grid(column=0, row=0, columnspan=2)

        verification_code = tk.CTkLabel(self, text='Codigo de verificação: ', font=f_font)
        verification_code.grid(column=0, row=1, columnspan=2, sticky='nw', pady=15)

        self.entry_code = tk.CTkEntry(self, placeholder_text='Code..', width=300)
        self.entry_code.grid(column=0, row=2, columnspan=2, pady=5)

        button_send = tk.CTkButton(self, font=b_font, text='Enviar', command=lambda: self.check_code())
        button_send.grid(column=0, row=3, pady=20)

        button_back = tk.CTkButton(self, font=b_font, text='Voltar',
                                   command=lambda: self.master.show_frame(LoginScreen))
        button_back.grid(column=1, row=3, pady=20)

    def check_code(self) -> None:
        global code
        global email_check
        global password_check
        print(email_check, password_check)

        if self.entry_code.get() is None or self.entry_code.get() == '':
            messagebox.showinfo('Info', 'Código invalido!')
            return None

        if EmailBackendOnyx.check_code(code) and email_check != '' and password_check != '':
            u = User(email_check, password_check)
            email_check = ''
            password_check = ''
            ret = u.insert_user()
            messagebox.showinfo('Info', ret)
            self.master.initial_frame()
            return None

        if EmailBackendOnyx.check_code(code):
            self.master.show_frame(ChangePasswordScreen)
            return None
        else:
            messagebox.showerror('Info', 'Codigo invalido!')
            return None


class ChangePasswordScreen(tk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        b_font, t_font, f_font = fonts()

        text_principal = tk.CTkLabel(self, text='Recuperação de senha!', font=t_font)
        text_principal.grid(column=0, row=0, columnspan=2)

        password_label = tk.CTkLabel(self, text='Digite a senha:', font=f_font)
        password_label.grid(column=0, row=1, columnspan=2, sticky='nw', pady=15)

        self.password_entry = tk.CTkEntry(self, placeholder_text='Senha...', width=300, show='*')
        self.password_entry.grid(column=0, row=2, columnspan=2, pady=5)

        password_confirm_label = tk.CTkLabel(self, text='Confirme a senha:', font=f_font)
        password_confirm_label.grid(column=0, row=3, columnspan=2, sticky='nw', pady=10)

        self.password_confirm_entry = tk.CTkEntry(self, width=300, placeholder_text='Confime a senha...', show='*')
        self.password_confirm_entry.grid(column=0, row=4, columnspan=2, pady=5)

        button_send = tk.CTkButton(self, font=b_font, text='Enviar', command=lambda: self.on_click_change())
        button_send.grid(column=0, row=5, pady=20)

        button_back = tk.CTkButton(self, font=b_font, text='Voltar',
                                   command=lambda: self.master.show_frame(LoginScreen))
        button_back.grid(column=1, row=5, pady=20)

    def on_click_change(self):
        if self.password_entry.get() == self.password_confirm_entry.get():
            ret = User.change_password(password=self.password_entry.get().encode())
            if ret:
                messagebox.showinfo('Info', 'Senha alterada com sucesso!')
                self.master.show_frame(LoginScreen)
                return None
            else:
                messagebox.showerror('ERROR', 'Ocorreu um erro tente novamente.')
        else:
            messagebox.showerror('ERROR', 'As senhas estão diferentes!')
            return None


