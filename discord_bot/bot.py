import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

from discord_bot.helpers import load_opus


class Bot(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)
        self.load_extension('cogs')

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
            return

        await self.process_commands(message)

    async def on_command_error(self, context, exception):
        if isinstance(exception, CommandNotFound):
            await context.message.channel.send(f"I don't know the command `{context.message.content}`", delete_after=10)
            await context.message.delete()
        else:
            raise exception
