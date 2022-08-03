import asyncio
from datetime import datetime
import discord
from discord.ext import commands

from modules.RawCommands import RawCommands

class Basic(commands.Cog, RawCommands):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now()

    @commands.command(help='Shows time to response')
    async def ping(self, ctx):
        await ctx.send(await self.ping_command())

    @commands.command(help='Shows uptime in format dddd:hh:mm:ss' ,)
    async def uptime(self, ctx): 
        await ctx.send(await self.uptime_command())