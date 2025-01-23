from src._databases import DataBases
from bcrypt import hashpw, checkpw, gensalt
from src._functions import check_email, set_time
from typing import Tuple, Union


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


if __name__ == '__main__':
    u = User('admin@admin.com', 'admin')
    u.insert_user(perm=3)
