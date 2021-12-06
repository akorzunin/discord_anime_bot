import asyncio

import discord
import youtube_dl

import bot_token

from Basic_commands import Basic
from Anime_Pic import AnimePic
from Music_commands import Music

from anime_picture import AnimePicture
from categories_list import categories, nsfw_categories

from datetime import datetime
from time import sleep

from discord.ext import commands
import platform

a = AnimePicture()
PREFIX = '.'
# PREXIX = os.getenv('PREFIX')


# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''
if platform.system() == "Windows":
    FFMPEG_BIN_PATH = "C:/PATH_programms/ffmpeg.exe"
    # FFMPEG_BIN_PATH = os.getenv('FFMPEG_BIN_PATH')
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
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

bot = commands.Bot(command_prefix=commands.when_mentioned_or(f"{PREFIX}"),
                   description='description')

# not working w/ client
@bot.listen('on_message')
async def on_message(message):
    if message.author == bot.user:
        return
    # user <@!{int}> 
    # role <@&{int}>
    if message.content.startswith(f'{PREFIX}<@'):
        print(message.content)
        await message.channel.send(f'{a.get_url()}')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

bot.add_cog(Basic(bot))
bot.add_cog(Music(bot))
bot.add_cog(AnimePic(bot))
bot.run(bot_token.token)
# need pynacl