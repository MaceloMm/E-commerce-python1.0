import os

STATIC_PATH = os.path.join(os.getcwd(), 'static\\')
DATABASE_PATH = os.path.join(os.getcwd(), 'databases\\')


if __name__ == '__main__':
    print(STATIC_PATH + '\n' + DATABASE_PATH)
