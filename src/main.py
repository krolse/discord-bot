import discord
from definitions import ROOT_PATH


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == '!ping':
            await message.channel.send('pong')


if __name__ == '__main__':
    def read_token():
        with open(f'{ROOT_PATH}/token', 'r') as file:
            return file.read()

    token = read_token()
    client = MyClient()
    client.run(token)
