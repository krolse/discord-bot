import asyncio

import discord
from discord import ClientException
from discord.opus import OpusNotLoaded
from discord_bot.helpers import import_sounds, load_opus
from definitions import PREFIX, ROOT_PATH


class Client(discord.Client):
    def __init__(self):
        super().__init__()
        self.sounds = import_sounds()

    async def add_sound(self, message: discord.Message):
        if message.attachments:
            for attachment in message.attachments:
                await attachment.save(f'{ROOT_PATH}/sounds/{attachment.filename}', use_cached=True)
        attachments_string = ",".join([attachment.filename for attachment in message.attachments])
        print(f'Saved attachments: {attachments_string}')
        await message.channel.send(f'Saved sound{"s" if len(message.attachments) > 1 else ""}: {attachments_string}')
        await message.delete()
        self.sounds = import_sounds()
        return

    @staticmethod
    async def play_sound(message):
        try:
            voice_channel = message.author.voice.channel
            await message.delete()
        except AttributeError:
            await message.channel.send('You\'re not in a voice channel, ya frig.')
            await message.delete()
            return
        if voice_channel:
            voice = await voice_channel.connect()
            try:
                voice.play(discord.FFmpegPCMAudio(f'{ROOT_PATH}/sounds/{message.content[1:]}.mp3'))
                while voice.is_playing():
                    await asyncio.sleep(0.1)
                await voice.disconnect()

            except ClientException:
                print("Already playing audio or not connected")
            except TypeError:
                print("Source is not an audio source or 'after' is not callable")
            except OpusNotLoaded:
                print("Source is not opus encoded and opus is not loaded")
            except (ClientException, OpusNotLoaded, TypeError):
                await voice.disconnect()

    async def on_ready(self):
        print('Logged on as', self.user)
        load_opus()

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        if message.content == f'{PREFIX}ping':
            await message.channel.send('pong')

        if message.content == f'{PREFIX}østers':
            await message.channel.send('> *Av østers får man sår <:nik:268402644966572032>*')
            await message.delete()

        if message.content == f'{PREFIX}lår':
            await message.channel.send('> *Har du lysk, har du lår <:nik:268402644966572032>*')
            await message.delete()

        if message.content == f'{PREFIX}hsl':
            with open(f'{ROOT_PATH}/secret/hsl', 'r') as hsl:
                await message.channel.send(f'{hsl.read()}', delete_after=20)
            await message.delete()

        if message.content.startswith(f'{PREFIX}addsound'):
            await self.add_sound(message)

        if message.content.startswith(PREFIX) and message.content[1:] in self.sounds:
            await Client.play_sound(message)
