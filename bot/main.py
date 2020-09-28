from bot.client import Client
from definitions import ROOT_PATH

if __name__ == '__main__':
    with open(f'{ROOT_PATH}/secret/token', 'r') as token:
        bot = Client()
        Client().run(token.read())
