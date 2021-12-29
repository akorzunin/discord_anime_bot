from urllib.parse import uses_fragment
import discord
from discord.ext import commands
from anime_picture import AnimePicture
from categories_list import categories, nsfw_categories
from time import sleep
from datetime import datetime
import bot_token

MSG_DELAY  = 1

# client = discord.Client()
start_time = datetime.today()
bot = commands.Bot(command_prefix='>')
a = AnimePicture()

# @bot.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(bot))

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return

#     # if message.content.startswith('>ping'):
#     #     await message.channel.send(f'ping: {random.randint(100, 200)}')

#     if message.content.startswith('<@'):
#         print(message.content)
#         await message.channel.send(f'{a.get_url()}')

@bot.command(help='champ')
async def pog(ctx):
    await ctx.send('champ')

@bot.command(help='Shows time to response')
async def ping(ctx):
    time_to_response = round(bot.latency * 1000)
    await ctx.send(f'{datetime.today()} ping: {time_to_response}ms')

@bot.command(help='{category}(see list w/ >gc), {amount}(max 30) Shows anime picture(s) with waifu',aliases=['gw'])
# get_waifu (self, )
async def get_waifu(ctx, category: str=None, amount: int=None):
    # TODO refactor
    if (amount != None) and (category != None):
        data = a.get_urls(amount, category=category)
        for i in data:
            await ctx.send(i)
            sleep(MSG_DELAY)
    else: 
        data = a.get_url(category)
        await ctx.send(data)

@bot.command(help='Shows avaliable categories' , aliases=['gc'])
async def get_categories(ctx):

    await ctx.send(categories)

@bot.command(help='Shows uptime in format dddd:hh:mm:ss' ,)
async def uptime(ctx):
    u = datetime.today() - start_time
    upt = u.seconds
    days = upt//(60*60*24) # dddd
    hours = upt//(60*60) - days*24 # hh
    minutes = upt//(60) - hours*60 - days*24*60# mm
    seconds = upt - minutes*60 - hours*60*60 - days*60*60*24 #ss

    uptime_ = f'uptime: {days}:{hours}:{minutes}:{seconds}'
    await ctx.send(uptime_)

@bot.command(help='at', aliases=['<@'])
async def at(ctx):
    await ctx.send('<@>')

token = bot_token.token
bot.run(token)
# client.run(token)