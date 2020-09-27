import asyncio

import discord
from discord import ClientException
from discord.opus import OpusNotLoaded

from definitions import PREFIX, ROOT_PATH
from bot.helpers import import_sounds, load_opus


class Client(discord.Client):
    def __init__(self):
        super().__init__()
        self.sounds = import_sounds()

    async def on_ready(self):
        print('Logged on as', self.user)
        load_opus()

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == f'{PREFIX}ping':
            await message.channel.send('pong')

        if message.content[1:] in self.sounds:
            voice_channel = message.author.voice.channel
            if voice_channel:
                voice = await voice_channel.connect()
                try:
                    voice.play(discord.FFmpegPCMAudio(f'{ROOT_PATH}/sounds/{message.content[1:]}.mp3'))
                    while voice.is_playing():
                        await asyncio.sleep(0.1)
                    await voice.disconnect()

                except ClientException:
                    print("Already playing audio or not connected")
                    await voice.disconnect()
                except TypeError:
                    print("Source is not an audio source or 'after' is not callable")
                    await voice.disconnect()
                except OpusNotLoaded:
                    print("Source is not opus encoded and opus is not loaded")
                    await voice.disconnect()
