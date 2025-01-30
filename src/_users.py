from src._databases import DataBases
from bcrypt import hashpw, checkpw, gensalt
from src._functions import check_email, set_time
from typing import Tuple, Union, Generator


class User:

    db = DataBases()
    cursor = db.get_cursor

    def __init__(self, email: str, password: str) -> None:
        if not check_email(email):
            raise ValueError('Email invalido!')
        self.__email: str = email.lower()
        self.__password: bytes = hashpw(password.encode(), gensalt())

    def insert_user(self, perm: int = 2) -> str:
        """

        :return:
        """
        try:

            exists = User.cursor.execute(
                """
                SELECT UserEmail FROM users WHERE UserEmail = ?;
                """, (self.__email,)
            ).fetchone()

            if exists:
                return 'Email já cadastrado!'

            tempo = set_time()

            User.cursor.execute(
                """
                INSERT INTO users (UserEmail, UserPassword, Status, TypeID, CreateAT, Alteration) VALUES (
                ?, ?, ?, ?, ?, ?);
                """, (self.__email, self.__password, True, perm, tempo, tempo)
            )

            User.db.commit_changes()

        except User.db.exepitons_returns():
            return 'Ocorreu um erro no cadastro!'
        else:
            return 'Usuário cadastrado com sucesso!'

    @staticmethod
    def check_password(email: str, password: bytes) -> Union[Tuple[bool, str], str]:
        """

        :param email:
        :param password:
        :return:
        """

        u = User.cursor.execute(
            """
            SELECT users.UserPassword, TypeUsers.TypeName, users.Status FROM users
            JOIN TypeUsers ON users.TypeID = TypeUsers.TypeID
            WHERE users.UserEmail = ?;
            """, (email.lower(),)
        ).fetchone()

        if u:
            if int(u[2]) != 1:
                return 'Usuario consta desativado!'
            if checkpw(password, u[0]):
                return True, u[1]
            else:
                return 'Senha invalida!'
        else:
            return 'Email não encontrado'

    @staticmethod
    def list_users() -> Union[str, None, Generator]:

        try:
            ret = User.cursor.execute(
                """
                SELECT UserEmail FROM users WHERE Status = True;
                """
            ).fetchall()
        except User.db.exepitons_returns() as err:
            return 'Ocorreu um erro na cosulta'
        else:
            return (i[0] for i in ret) if len(ret) != 0 else None

    @staticmethod
    def change_password(password: bytes) -> bool:

        try:
            password = hashpw(password, gensalt())
            User.cursor.execute(
                """
                UPDATE users SET UserPassword = ?;
                """, (password, )
            )
        except User.db.exepitons_returns():
            return False
        else:
            return True


if __name__ == '__main__':
    print(User.list_users())
