

def check_email(email: str) -> bool:
    """
    Função responsavel por validar se uma string está em formato de Email.

    :param email: String a ser verificada se está em um formato de E-mail
    :return: Retorna se o Email e valido ou não
    """

    email = email.replace(' ', '').strip()
    requeriments = ('.com', '@')
    for i in requeriments:
        if i in email:
            pass
        else:
            return False
    return True