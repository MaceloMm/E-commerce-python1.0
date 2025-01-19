from datetime import datetime
import requests
from typing import Union
import customtkinter as tk


def check_email(email: str) -> bool:
    """
    Função responsavel por validar se uma string está em formato de Email.

    :param email: String a ser verificada se está em um formato de E-mail
    :return: Retorna se o Email e valido ou não
    """

    email = email.replace(' ', '').strip()
    requeriments = ('.com', '@')
    for i in requeriments:
        if i not in email:
            return False
    return True


def set_time() -> str:
    return datetime.now().strftime("%Y/%m/%dT| %H:%M:%S")


def format_adress(adress: dict, num: int) -> dict:
    """
    Fução responsavel por inserir o numero da casa/predio no endereço do cliente

    :param adress: endereço sem o numero
    :param num: numero da casa/predio
    :return: retorna o endereço completo do cliente
    """
    if num == '' or num is None:
        raise ValueError('Numero invalido')
    adress['numero'] = num
    return adress


def get_cep_infos(cep: str) -> Union[str, dict]:
    """
    Função responsavel por verificar se o CEP e valido e retorna as informações de
    (CEP, Logadouro, bairro, localidade, uf, estado)

    :param cep: CEP informado pelo usuario
    :return: (CEP, Logadouro, bairro, localidade, uf, estado) caso seja invalido retorna que o CPF e invalido
    """

    if cep == '' or cep is None:
        raise ValueError('CEP está vazio!')

    exclude_itens: tuple = ('complemento', 'unidade', 'regiao', 'ibge', 'gia', 'ddd', 'siafi')
    cep = cep.replace('-', '').replace('.', '').replace(' ', '').strip()

    url = f'https://viacep.com.br/ws/{cep}/json/'

    response = requests.get(url)
    adress = response.json()

    if response.status_code != 200 or 'erro' in adress:
        return 'CEP invalido!'

    for i in exclude_itens:
        adress.pop(i)

    return adress


def fonts():
    buttons_fonts = tk.CTkFont(size=14, weight='bold', family='Arial')
    title_font = tk.CTkFont(size=20, weight='bold', family='Arial')
    topic_font = tk.CTkFont(size=13, weight='bold', family='Arial')

    return buttons_fonts, title_font, topic_font


if __name__ == '__main__':
    print(get_cep_infos('06326488'))

