import asyncio

import discord
from discord import ClientException
from discord.opus import OpusNotLoaded
from discord.ext import commands
from discord_bot.helpers import import_sounds, load_opus
from definitions import ROOT_PATH


class Bot(commands.Bot):
    class Sound(commands.Cog):
        def __init__(self, bot):
            self.bot = bot
            self.sounds = import_sounds()

        @commands.command(name='addsound')
        async def add_sound(self, ctx: commands.Context):
            if ctx.message.attachments:
                for attachment in ctx.message.attachments:
                    await attachment.save(f'{ROOT_PATH}/sounds/{attachment.filename}', use_cached=True)
            attachments_string = ",".join([attachment.filename for attachment in ctx.message.attachments])
            print(f'Saved attachments: {attachments_string}')
            await ctx.message.channel.send(
                f'Saved sound{"s" if len(ctx.message.attachments) > 1 else ""}: {attachments_string}')
            await ctx.message.delete()
            self.sounds = import_sounds()
            return

        @staticmethod
        async def play_sound(message: discord.Message):
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

    class Misc(commands.Cog):
        def __init__(self, bot):
            self.bot = bot

        @commands.command(name='østers')
        async def oyster(self, ctx: commands.Context):
            await ctx.send('> *Av østers får man sår <:nik:268402644966572032>*')
            await ctx.message.delete()
            print("hello")

        @commands.command()
        async def lysk(self, ctx: commands.Context):
            await ctx.send('> *Har du lysk, har du lår <:nik:268402644966572032>*')
            await ctx.message.delete()

        @commands.command()
        async def hsl(self, ctx: commands.Context):
            with open(f'{ROOT_PATH}/secret/hsl', 'r') as hsl:
                await ctx.send(f'{hsl.read()}', delete_after=20)
            await ctx.message.delete()

    def __init__(self, command_prefix):
        super().__init__(command_prefix=command_prefix)
        self.add_cog(self.Sound(self))
        self.add_cog(self.Misc(self))

    def _is_play_sound_command(self, message: discord.Message):
        return message.content.startswith(self.command_prefix) and message.content[1:] in self.get_cog('Sound').sounds

    async def on_ready(self):
        print('Logged on as', self.user)
        load_opus()

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        if self._is_play_sound_command(message):
            await self.get_cog('Sound').play_sound(message)
