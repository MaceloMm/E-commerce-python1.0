from random import randint
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src._functions import format_static_path
from typing import Tuple, Union


class EmailBackendOnyx:
    """
    Classe responsavel pelo o envio de Emails.
    """

    random_code = 0

    EMAIL_HOST = 'smtp.gmail.com'  # Servidor SMTP do Gmail
    EMAIL_PORT = 587  # Porta para TLS
    EMAIL_HOST_USER = 'maceloaugusto066@gmail.com'  # Seu e-mail
    EMAIL_HOST_PASSWORD = 'fkox nehf islh hvda' # Senha de aplicativo

    @classmethod
    def send_email(cls, email_dest: str) -> Union[Tuple[str, str], str]:
        cls.random_code = str(randint(111111, 999999))
        with open(format_static_path('email', 'template.html'), 'r', encoding='utf-8') as file:
            html_template = file.read().replace('?randomcode?', cls.random_code)

        mensagem = MIMEMultipart()
        mensagem["From"] = cls.EMAIL_HOST_USER
        mensagem["To"] = email_dest
        mensagem["Subject"] = "Codigo de verificação!"
        mensagem.attach(MIMEText(html_template, 'html'))

        try:
            with smtplib.SMTP(cls.EMAIL_HOST, cls.EMAIL_PORT) as server:
                server.starttls()
                server.login(cls.EMAIL_HOST_USER, cls.EMAIL_HOST_PASSWORD)
                server.sendmail(cls.EMAIL_HOST_USER, email_dest, mensagem.as_string())
        except Exception as err:
            return 'Ocorreu um erro'
        else:
            return cls.random_code, 'Email enviado!'

    @classmethod
    def check_code(cls, code: str) -> bool:
        return True if cls.random_code == code else False


if __name__ == '__main__':
    EmailBackendOnyx.send_email('macelogamer056@gmail.com')
    print(EmailBackendOnyx.check_code(input('Digite o codigo: ')))