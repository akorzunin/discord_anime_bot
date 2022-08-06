import asyncio
import logging
import platform
import random
import discord
import requests
import youtube_dl
from discord.ext import tasks
from discord.ext.commands import CommandError
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

class YTDLSource(discord.PCMVolumeTransformer):
    ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: cls.ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else cls.ytdl.prepare_filename(data)
        if platform.system() == "Windows":
            return cls(discord.FFmpegPCMAudio(filename, executable=FFMPEG_BIN_PATH, **ffmpeg_options), data=data)
        else: return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Sound():
    YTDLSource = YTDLSource
    default_volume = 80
    current_volume = None

    @classmethod
    def set_default_volume(cls, volume: int):
        cls.default_volume = volume

    @tasks.loop(count=1)
    async def setup_disconnect_timer(self, ctx):
        await asyncio.sleep(300)
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send('Disconnected due to inactivity')
        if self.wathchdog_timer.is_running():
            self.wathchdog_timer.stop()

    @tasks.loop(seconds=60)
    async def wathchdog_timer(self, ctx):
        # sourcery skip: merge-nested-ifs
        if ctx.voice_client:
            if not ctx.voice_client.is_playing():
                self.setup_disconnect_timer.start(ctx)
                self.wathchdog_timer.stop()

    async def _leave_voice(self, ctx):
        if not self.wathchdog_timer.is_running():
            self.wathchdog_timer.start(ctx)

    async def _ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
                return
            await ctx.send("You are not connected to a voice channel.")
            raise CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            return
        self.setup_disconnect_timer.cancel()
