import asyncio

import discord

from datetime import datetime
from time import sleep

from modules.db_connector import db, memes

from discord.ext import commands
class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now()

    @commands.command(help='')
    async def db_conn(self, ctx):
        # time_to_response = round(self.bot.latency * 1000)
        a = memes.insert(dict(name='1mem', pog=[1,2,3]))
        await ctx.send(a)

    @commands.command(help='Shows time to response')
    async def ping(self, ctx):
        time_to_response = round(self.bot.latency * 1000)
        await ctx.send(f'{datetime.now()} ping: {time_to_response}ms')

    @commands.command(help='Shows uptime in format dddd:hh:mm:ss' ,)
    async def uptime(self, ctx):  # sourcery skip: square-identity
        u = datetime.now() - self.start_time
        upt = u.seconds
        days = upt//(60*60*24) # dddd
        hours = upt//(60*60) - days*24 # hh
        minutes = upt//(60) - hours*60 - days*24*60# mm
        seconds = upt - minutes*60 - hours*60*60 - days*60*60*24 #ss

        uptime_ = f'uptime: {days}:{hours}:{minutes}:{seconds}'
        await ctx.send(uptime_)