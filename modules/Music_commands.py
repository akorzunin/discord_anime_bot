import asyncio
import logging
import platform
import random
import discord
import requests
import youtube_dl

from Basic_commands import Basic
from Anime_Pic import AnimePic
from Gachi_handler import GachiHandler

from datetime import datetime
from time import sleep

from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands.errors import CommandInvokeError

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''
if platform.system() == "Windows":
    FFMPEG_BIN_PATH = "C:/PATH_programms/ffmpeg.exe"

# MSG_DELAY  = 1

# start_time = datetime.today()


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0', # bind to ipv4 since ipv6 addresses cause issues sometimes
    # 'cachedir': r'dl_cachedir' # not working
    'buffersize': 1024*8, #not helping
    # download_archive:


    # geo_bypass:        Bypass geographic restriction via faking X-Forwarded-For
    #                    HTTP header
    # geo_bypass_country:
    #                    Two-letter ISO 3166-2 country code that will be used for
    #                    explicit geographic restriction bypassing via faking
    #                    X-Forwarded-For HTTP header
    # geo_bypass_ip_block:
    #                    IP range in CIDR notation that will be used similarly to
    #                    geo_bypass_country

    # The following parameters are not used by YoutubeDL itself, they are used by
    # the downloader (see youtube_dl/downloader/common.py):
    # buffersize

        # ffmpeg_location:   Location of the ffmpeg/avconv binary; either the path
        #                to the binary or its containing directory.
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        if platform.system() == "Windows":
            return cls(discord.FFmpegPCMAudio(filename, executable=FFMPEG_BIN_PATH, **ffmpeg_options), data=data)
        else: return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.default_volume = 3
        self.current_volume = None
        self.g = GachiHandler()
        # self.loop_flag = False
        


    # # @staticmethod
    # def change_volume(self, obj, volume=None):
    #     if volume is None: volume = self.default_volume
    #     obj = volume / 100
    #     self.current_volume = volume
    #     return self.current_volume

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""
        # def repeat(guild, voice, audio):
        #     # voice.play(audio, after=lambda e: repeat(guild, voice, audio))
        #     # voice.is_playing()
        #     pass
        # voice = get(self.bot.voice_clients, guild=ctx.guild)
        if platform.system() == "Windows":
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query, executable=FFMPEG_BIN_PATH))
        else: source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query,))
        # if self.loop_flag:
        #     pass
        #     # ctx.voice_client.play(source, after=lambda e: repeat(ctx.guild, ctx.voice_client, source))
        # else:
        ctx.voice_client.play(source, after=lambda e: logging.debug(f'Player error: {e}') if e else None)
        ctx.voice_client.source.volume = self.default_volume / 100
        await ctx.send(f'Now playing: {query}')

    # @commands.command()
    # async def play(self, ctx, *, query):
    #     """Plays a file from the local filesystem"""
    #     # def repeat(guild, voice, audio):
    #     #     # voice.play(audio, after=lambda e: repeat(guild, voice, audio))
    #     #     # voice.is_playing()
    #     #     pass
    #     # voice = get(self.bot.voice_clients, guild=ctx.guild)
    #     source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query, executable=FFMPEG_BIN_PATH))
    #     # if self.loop_flag:
    #     #     pass
    #     #     # ctx.voice_client.play(source, after=lambda e: repeat(ctx.guild, ctx.voice_client, source))
    #     # else:
    #     ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
    #     ctx.voice_client.source.volume = self.default_volume / 100
    #     await ctx.send(f'Now playing: {query}')
    # @commands.command()
    # async def play(self, ctx, *, query):
    #     await ctx.channel.purge(limit=1)
    #     channel = ctx.author.voice.channel
    #     voice = get(self.bot.voice_clients, guild=ctx.guild)

    #     def repeat(guild, voice, audio):
    #         voice.play(audio, after=lambda e: repeat(guild, voice, audio))
    #         voice.is_playing()

    #     if channel and not voice.is_playing():
    #         audio = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query, executable=FFMPEG_BIN_PATH))
    #         voice.play(audio, after=lambda e: repeat(ctx.guild, voice, audio))
    #         voice.is_playing()

    # region
    
    @commands.command(aliases=['gm'])
    async def gachi(self, ctx, *args):
        """Gachi command"""
        query = ' '.join(args)
        gachi_dict = self.g.validate_gachi(query)
        if len(gachi_dict) == 0: 
            await ctx.send('Not Found')
            return
        gachi_tuple = random.choice(list(gachi_dict.items()))
        url = f'http://soundboard.ass-we-can.com/static/music/{gachi_tuple[1]}/{gachi_tuple[0]}.mp3'
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: logging.debug(f'Player error: {e}') if e else None)
            ctx.voice_client.source.volume = self.default_volume / 100
            # change_volume(player, self.default_volume)
        await ctx.send(f'Now playing: {player.title}')


    # endregion

    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: logging.debug(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: logging.debug(f'Player error: {e}') if e else None)
            ctx.voice_client.source.volume = self.default_volume / 100
            # change_volume(player, self.default_volume)
        await ctx.send(f'Now playing: {player.title}')

    @commands.command(aliases=['vol'])
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command(aliases= ['dv', 'defvol'])
    async def default_volume(self, ctx, volume: int):
        """Changes the player's volume"""
        self.default_volume = volume
        await ctx.send(f"Changed default volume to {volume}%")
    # reset the volume to default

        
    @commands.command(aliases=['disconnect'])
    async def close(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    # buffer
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
    # @commands.command()
    # async def loop(self, ctx):
    #     """Loop player"""
    #     self.loop_flag = not self.loop_flag
    #     # ctx.voice_client.resume()
    #     await ctx.send(f'{self.loop_flag=}')

    @commands.command(aliases=['mjoin'])
    async def manual_join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def join(self, ctx):
        """Joins to sender voice channel"""
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command(aliases=['gv'])
    async def get_volume(self, ctx, ):
        """Return current volume level"""
        await ctx.send(f"Current volume: {ctx.voice_client.source.volume*100}\nDefault volume: {self.default_volume}")

     
    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    @gachi.before_invoke # move later
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
