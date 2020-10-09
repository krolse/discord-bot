from discord_bot.bot import Bot
from definitions import ROOT_PATH, PREFIX

if __name__ == '__main__':
    with open(f'{ROOT_PATH}/secret/token', 'r') as token:
        bot = Bot(PREFIX)
        bot.run(token.read())
