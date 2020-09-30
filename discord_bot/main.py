from discord_bot.bot import Bot
from discord_bot.client import Client
from definitions import ROOT_PATH, PREFIX

if __name__ == '__main__':
    with open(f'{ROOT_PATH}/secret/token', 'r') as token:
        Client().run(token.read())
