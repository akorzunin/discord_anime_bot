import asyncio
from datetime import datetime
import discord
from discord.ext import commands

from modules.RawCommands import RawCommands
from modules.db_connector import db, memes


class Basic(commands.Cog, RawCommands):
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
        await ctx.send(await self.ping_command())

    @commands.command(help='Shows uptime in format dddd:hh:mm:ss' ,)
    async def uptime(self, ctx): 
        await ctx.send(await self.uptime_command())