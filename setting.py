import os

STATIC_PATH = os.path.join(os.getcwd(), 'static\\').replace(
    'interface\\', '').replace('src\\', '')
DATABASE_PATH = os.path.join(os.getcwd(), 'databases\\').replace(
    'interface\\', '').replace('src\\', '').replace(
    'repository\\', '').replace('models\\', '').replace(
    'services\\', '')


if __name__ == '__main__':
    print(STATIC_PATH + '\n' + DATABASE_PATH)
