import asyncio
import logging
import platform
import discord
from discord.ext import commands, tasks

if platform.system() == "Windows":
    FFMPEG_BIN_PATH = "C:/PATH_programms/ffmpeg.exe"

class SoundCommads(commands.Cog): 
    '''docstring for SoundCommads'''
    def __init__(self, bot, sound):
        self.bot = bot
        self.sound = sound

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""
        if platform.system() == "Windows":
            source = discord.PCMVolumeTransformer(
                discord.FFmpegPCMAudio(query, executable=FFMPEG_BIN_PATH))
        else: source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(query,))
        ctx.voice_client.play(source, after=lambda e: logging.debug(
            f'Player error: {e}') if e else None)
        ctx.voice_client.source.volume = self.sound.default_volume / 100
        await ctx.send(f'Now playing: {query}')

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await self.sound.YTDLSource.from_url(
                url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: logging.debug(
                f'Player error: {e}') if e else None)
            ctx.voice_client.source.volume = self.sound.default_volume / 100
        await ctx.send(f'Now playing: {player.title}')

    @commands.command(aliases=['vol'])
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command(aliases= ['dv', 'defvol'])
    async def set_default_volume(self, ctx, volume: int):
        """Changes the player's volume"""
        self.sound.default_volume = volume
        await ctx.send(f"Changed default volume to {volume}%")

    @commands.command(aliases=['disconnect', 'leave'])
    async def close(self, ctx):
        """Stops and disconnects the bot from voice"""
        await ctx.voice_client.disconnect()

    @commands.command()
    async def buffer(self, ctx, wait_time: int=5):
        """Bufferize stream (can take int [seconds])"""
        msg = await ctx.send('Buffering...')
        ctx.voice_client.pause()
        await asyncio.sleep(wait_time)
        ctx.voice_client.resume()
        await msg.edit(content='Done')
        # await ctx.send('Done')

    @commands.command(aliases=['halt'])
    async def stop(self, ctx):
        """Stops player"""
        ctx.voice_client.stop()
        await ctx.send('Stopped')

    @commands.command()
    async def pause(self, ctx):
        """Pause player"""
        ctx.voice_client.pause()
        await ctx.send('Paused')

    @commands.command()
    async def resume(self, ctx):
        """Resume player"""
        ctx.voice_client.resume()
        await ctx.send('Resumed')

    @commands.command(aliases=['mjoin'])
    async def manual_join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def join(self, ctx):
        """Joins to sender voice channel"""
        if voice := ctx.author.voice:
            await voice.channel.connect()
            self.sound.setup_disconnect_timer.start(ctx)


    @commands.command(aliases=['gv'])
    async def get_volume(self, ctx, ):
        """Return current volume level"""
        await ctx.send(f"Current volume: {ctx.voice_client.source.volume*100}\nDefault volume: {self.sound.default_volume}")
    
    @play.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
                return
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            return

        self.sound.setup_disconnect_timer.cancel()

    @play.after_invoke
    @stream.after_invoke
    async def leave_voice(self, ctx):
        self.sound.wathchdog_timer.start(ctx)