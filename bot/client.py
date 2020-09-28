import asyncio

import discord
from discord import ClientException
from discord.opus import OpusNotLoaded

from bot.helpers import import_sounds, load_opus
from definitions import PREFIX, ROOT_PATH


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

        if message.content == f'{PREFIX}østers':
            await message.channel.send('> *Av østers får man sår <:nik:268402644966572032>*')
            await message.delete()

        if message.content == f'{PREFIX}hsl':
            with open(f'{ROOT_PATH}/secret/hsl', 'r') as hsl:
                await message.channel.send(f'{hsl.read()}')
            await message.delete()

        if message.content[1:] in self.sounds:
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
