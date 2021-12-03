import asyncio

import discord
import youtube_dl

from Basic_commands import Basic
from Anime_Pic import AnimePic
from datetime import datetime
from time import sleep

from discord.ext import commands


# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

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
        return cls(discord.FFmpegPCMAudio(filename, executable=FFMPEG_BIN_PATH, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.default_volume = 3
        self.current_volume = None

    # # @staticmethod
    # def change_volume(self, obj, volume=None):
    #     if volume is None: volume = self.default_volume
    #     obj = volume / 100
    #     self.current_volume = volume
    #     return self.current_volume

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query, executable=FFMPEG_BIN_PATH))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
        ctx.voice_client.source.volume = self.default_volume / 100
        await ctx.send(f'Now playing: {query}')

    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
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
        
    @commands.command(aliases=['disconnect'])
    async def close(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

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
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command(aliases=['gv'])
    async def get_volume(self, ctx, ):
        """Return current volume level"""
        await ctx.send(f"Current volume: {ctx.voice_client.source.volume*100}\nDefault volume: {self.default_volume}")
        
    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
