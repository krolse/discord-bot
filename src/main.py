from definitions import ROOT_PATH
from src.client import Client


if __name__ == '__main__':
    with open(f'{ROOT_PATH}/token', 'r') as token:
        Client().run(token.read())
