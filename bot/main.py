from definitions import ROOT_PATH
from bot.client import Client


if __name__ == '__main__':
    with open(f'{ROOT_PATH}/token', 'r') as token:
        bot = Client()
        Client().run(token.read())
