from src._databases import DataBases
from bcrypt import hashpw, checkpw, gensalt
from src._functions import check_email, set_time


class User:

    db = DataBases()
    cursor = db.get_cursor

    def __init__(self, email: str, password: str) -> None:
        if not check_email(email):
            raise ValueError('Email invalido!')
        self.__email: str = email.lower()
        self.__password: bytes = hashpw(password.encode(), gensalt())

    def insert_user(self) -> str:
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
            """, (self.__email, self.__password, True, 2, tempo, tempo)
        )

        User.db.commit_changes()

        return 'Usuário cadastrado com sucesso!'


if __name__ == '__main__':
    user = User('Macelo@macelo.com', 'macelo123')
    print(user.insert_user())
