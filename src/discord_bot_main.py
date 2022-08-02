import asyncio
import logging
import os
import youtube_dl
from tinydb import TinyDB, Query
import discord
from discord.ext import commands

from modules.BasicCommands import Basic
from modules.AnimePic import AnimePic
from modules.BotSlashCommands import BotSlashCommands
from modules.MusicCommands import Music
from modules.AnimeChCommands import AnimeCh
from modules.DailyTask import DailyTask
from modules.AnimePictureApi import AnimePicture
from modules.db_connector import db, memes, stickers
from static_data.guilds import knownd_guilds, debug_guild_id

#load .env variables
import os
from dotenv import load_dotenv
load_dotenv()

PWD = os.path.abspath(os.getcwd())
PREFIX = os.getenv('PREFIX', '.')
BOT_TOKEN = os.getenv('BOT_TOKEN')
LOGGING_LEVEL = int(os.getenv('LOGGING_LEVEL', logging.INFO))
DEBUG = bool(os.getenv('DEBUG')) 

format = '%(asctime)s [%(levelname)s]: %(message)s'
logger = logging.basicConfig(
    format=format,
    encoding='utf-8', 
    level=LOGGING_LEVEL, 
)



youtube_dl.utils.bug_reports_message = lambda: ''

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

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(f"{PREFIX}"),
    description='description',
    intents=discord.Intents.all(),    
)

a = AnimePicture()

@bot.listen('on_message')
async def on_message(message):
    if message.author == bot.user:
        return
        
    # user <@!{int}> 
    # role <@&{int}>
    if message.content.startswith(f'{PREFIX}<@'):
        # logging.debug(message.content)
        await message.channel.send(f'{a.get_url()}')
    #handle stickers
    if message.content.startswith(f'{PREFIX}:'):
        name = message.content.split(':')[1]
        image = stickers.search(Query().name == name)[0]['image']
        # await message.edit(content=image)
        await message.channel.send(image)


@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
    logging.info('------')
    await bot.tree.sync(guild=discord.Object(id=debug_guild_id))




async def launch_bot():

    if DEBUG:
        import nest_asyncio
        loop = asyncio.get_event_loop()
        nest_asyncio.apply(loop) 

    await bot.add_cog(
        BotSlashCommands(bot), 
        guilds=[discord.Object(id = guid_id) for guid_id in knownd_guilds]
    )
    await bot.add_cog(Basic(bot))
    await bot.add_cog(Music(bot))
    await bot.add_cog(AnimePic(bot))
    await bot.add_cog(AnimeCh(bot))
    await bot.add_cog(DailyTask(bot))

    await bot.start(BOT_TOKEN)
    
if __name__ == '__main__':
    asyncio.run(launch_bot())
