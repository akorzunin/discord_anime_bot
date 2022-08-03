from discord.ext import commands
import random
import logging

from modules.GachiHandler import GachiHandler
# from modules.MusicCommands import Music, YTDLSource
class GachiCommands(commands.Cog): 
    '''docstring for GachiCommands'''
    def __init__(self, bot, sound):
        self.bot = bot
        self.sound = sound
        self.g_handler = GachiHandler()

    @commands.command(aliases=['gm'])
    async def gachi(self, ctx, *args):
        """Gachi command"""
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
        await ctx.send(f'Now playing: {player.title}')

    @gachi.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            
    @gachi.after_invoke
    async def leave_voice(self, ctx):
        if self.sound.setup_disconnect_timer.is_running():
            self.sound.setup_disconnect_timer.restart(ctx)
            return
        self.sound.setup_disconnect_timer.start(ctx)
