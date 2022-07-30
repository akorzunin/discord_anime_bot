import asyncio
import discord
from datetime import datetime
from requests import get


from discord.ext import commands


class AnimeCh(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now()

    @commands.command(help='Shows link to a host', aliases=['ac'])
    async def anime_challenge(self, ctx):
        host_ip = get('https://api.ipify.org').content.decode('utf8')
        await ctx.send(f'At {datetime.now()} \nCurrent host location is: http://{host_ip}:5050/')

