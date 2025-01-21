from src._databases import DataBases


class User:

    cursor = DataBases().get_cursor

    def __init__(self):
        pass
