import asyncio
import logging

import discord
import youtube_dl
import os
PWD = os.path.abspath(os.getcwd())
print(PWD)



from modules.Basic_commands import Basic
from modules.Anime_Pic import AnimePic
from modules.Music_commands import Music
from modules.anime_ch_commands import AnimeCh
from modules.Daily_Task import DailyTask
from modules.anime_picture import AnimePicture

from static_data.categories_list import categories, nsfw_categories

from datetime import datetime
from time import sleep

from discord.ext import commands
import platform

#load .env variables
import os
from dotenv import load_dotenv
load_dotenv()

PREFIX = os.getenv('PREFIX', '.')
BOT_TOKEN = os.getenv('BOT_TOKEN')
FFMPEG_BIN_PATH = os.getenv('FFMPEG_BIN_PATH', None)
LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', logging.INFO)

import logging
DEBUG = __debug__ 
LOG_FILE_NAME = 'logs.log'
format = '%(asctime)s [%(levelname)s]: %(message)s'
logger = logging.basicConfig(
    filename=LOG_FILE_NAME if not DEBUG else None, 
    format=format,
    encoding='utf-8', 
    level=LOGGING_LEVEL, 
)
if not DEBUG:
    logging.getLogger(logger).addHandler(logging.StreamHandler())


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

a = AnimePicture()

@bot.listen('on_message')
async def on_message(message):
    if message.author == bot.user:
        return
        
    # user <@!{int}> 
    # role <@&{int}>
    if message.content.startswith(f'{PREFIX}<@'):
        logging.debug(message.content)
        await message.channel.send(f'{a.get_url()}')

@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
    logging.info('------')
    

bot.add_cog(Basic(bot))
bot.add_cog(Music(bot))
bot.add_cog(AnimePic(bot))
bot.add_cog(AnimeCh(bot))
bot.add_cog(DailyTask(bot))

bot.run(BOT_TOKEN)
# need pynacl