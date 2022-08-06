import asyncio
import logging
from operator import truediv
import os
import youtube_dl
from tinydb import TinyDB, Query
import discord
from discord.ext import commands

from modules.Sound import Sound
from modules.BasicCommands import Basic
from modules.AnimePic import AnimePic
from modules.BotSlashCommands import BotSlashCommands
from modules.GachiCommands import GachiCommands
from modules.AnimeChCommands import AnimeCh
from modules.DailyTask import DailyTask
from modules.AnimePictureApi import AnimePicture
from modules.SoundCommands import SoundCommads
from modules.StickerSlashCommands import StickerSlashCommands
from modules.db_connector import stickers
from static_data import guilds

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

intents = discord.Intents.default()
# intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(f"{PREFIX}"),
    description='description',
    intents=intents,    
)

a = AnimePicture()

@bot.listen('on_message')
async def on_message(message):
    if message.author == bot.user:
        return
        
    # user <@!{int}> 
    # role <@&{int}>
    if message.content.startswith(f'{PREFIX}<@'):
        await message.channel.send(f'{a.get_url()}')
    #handle stickers
    if message.content.startswith(f'{PREFIX}:'):
        name = message.content.split(':')[1]
        image = stickers.search(Query().name == name)[0]['image']
        await message.channel.send(image)


@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
    logging.info('------')
    await bot.tree.sync(guild=discord.Object(id=guilds.debug_guild_id))
    await bot.tree.sync(guild=discord.Object(id=guilds.disboard))

async def add_slash_cog(bot, cog, *args):
    await bot.add_cog(
        cog(bot, *args), 
        guilds=[discord.Object(id = guid_id) 
            for guid_id in guilds.knownd_guilds]
    )


async def launch_bot():
    if DEBUG:
        import nest_asyncio
        loop = asyncio.get_event_loop()
        nest_asyncio.apply(loop) 

    sound = Sound()
    await add_slash_cog(bot, BotSlashCommands)
    await add_slash_cog(bot, StickerSlashCommands)
    await add_slash_cog(bot, SoundCommads, sound)
    await add_slash_cog(bot, GachiCommands, sound)

    await bot.add_cog(Basic(bot))
    await bot.add_cog(AnimePic(bot))
    await bot.add_cog(AnimeCh(bot))
    await bot.add_cog(DailyTask(bot))


    await bot.start(BOT_TOKEN)
    
if __name__ == '__main__':
    asyncio.run(launch_bot())
