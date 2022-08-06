import platform
import asyncio
import logging
import discord

if platform.system() == "Windows":
    FFMPEG_BIN_PATH = "C:/PATH_programms/ffmpeg.exe"

class RawSoundCommands(object): 
    '''docstring for RawSoundCommands'''
    async def get_ctx(self, interaction : discord.Interaction,):
        return await discord.ext.commands.Context.from_interaction(interaction)

    async def play_command(self, ctx, query):
        if platform.system() == "Windows":
            source = discord.PCMVolumeTransformer(
                discord.FFmpegPCMAudio(query, executable=FFMPEG_BIN_PATH))
        else: source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(query,))
        ctx.voice_client.play(source, after=lambda e: logging.debug(
            f'Player error: {e}') if e else None)
        ctx.voice_client.source.volume = self.sound.default_volume / 100

    async def stream_command(self, ctx, url):
        async with ctx.typing():
            player = await self.sound.YTDLSource.from_url(
                url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: logging.debug(
                f'Player error: {e}') if e else None)
            ctx.voice_client.source.volume = self.sound.default_volume / 100
        return player
        
    async def volume_command(self, ctx, volume):
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")
        ctx.voice_client.source.volume = volume / 100
        
    async def join_command(self, ctx):
        if voice := ctx.author.voice:
            await voice.channel.connect()
            self.sound.setup_disconnect_timer.start(ctx)