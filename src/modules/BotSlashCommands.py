from datetime import datetime
import discord
from discord import app_commands
from discord.ext import commands

from modules.RawCommands import RawCommands

class BotSlashCommands(commands.Cog, RawCommands): 
    '''docstring for BotSlashCommands'''
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now()

    @app_commands.command(name = "ping", description = "Retruns ping from bot host")
    async def ping(self, interaction : discord.Interaction, ):
        await interaction.response.send_message(await self.ping_command())

    @app_commands.command(name = "uptime", description = "Retruns bot uptime")
    async def uptime(self, interaction : discord.Interaction, ):
        await interaction.response.send_message(await self.uptime_command())


