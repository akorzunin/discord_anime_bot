from typing import Optional
import discord
from discord.ext import commands
from discord import app_commands
import random
import logging

from modules.GachiHandler import GachiHandler
# from modules.MusicCommands import Music, YTDLSource
class GachiCommands(commands.Cog, ): 
    '''docstring for GachiCommands'''
    def __init__(self, bot, sound):
        self.bot = bot
        self.sound = sound
        self.g_handler = GachiHandler()

    async def gachi_command(self, ctx, *args):
        query = ' '.join(args)
        gachi_dict = self.g_handler.validate_gachi(query)
        if len(gachi_dict) == 0: 
            await ctx.send('Not Found')
            return
        gachi_tuple = random.choice(list(gachi_dict.items()))
        url = f'http://soundboard.ass-we-can.com/static/music/{gachi_tuple[1]}/{gachi_tuple[0]}.mp3'
        async with ctx.typing():
            player = await self.sound.YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: logging.debug(f'Player error: {e}') if e else None)
            ctx.voice_client.source.volume = self.sound.default_volume / 100
            return player

    @commands.command(aliases=['gm'])
    async def gachi(self, ctx, *args):
        """Gachi command"""
        player = await self.gachi_command(ctx, *args)
        await ctx.send(f'Now playing: {player.title}')

    @app_commands.command(name='gachi_sound', description='Play a sound from gachi library')
    @app_commands.describe(query='query')
    # TODO add autocomplete
    async def slash_gashi(self, interaction: discord.Interaction, query: Optional[str] = ''):
        ctx = await discord.ext.commands.Context.from_interaction(interaction)
        await self._ensure_voice(ctx)
        player = await self.gachi_command(ctx, query)
        await interaction.followup.send(content=f'Now playing: {player.title}')
        await self._leave_voice(ctx)

    async def _ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    @gachi.before_invoke
    async def ensure_voice(self, ctx):
        await self._ensure_voice(ctx)

    async def _leave_voice(self, ctx):
        if self.sound.setup_disconnect_timer.is_running():
            self.sound.setup_disconnect_timer.restart(ctx)
            return
        self.sound.setup_disconnect_timer.start(ctx)

    @gachi.after_invoke
    async def leave_voice(self, ctx):
        await self._leave_voice(ctx)
