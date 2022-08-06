from datetime import datetime
import discord
from discord import app_commands
from discord.ext import commands

from modules.Buttons import BannerButtons, DetectorButtons
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


    @app_commands.command(name = "banner", description = "Creates a banner to ping all participants after")
    @app_commands.describe(role_name="New role")
    async def create_banner(self, interaction : discord.Interaction, role_name : str):
        await interaction.response.defer()
        # create new role if role name is unique
        same_roles = [i for i  in interaction.guild.roles if i.name == role_name]
        if not same_roles:
            new_role = await interaction.guild.create_role(name=role_name)
            view = BannerButtons(new_role)
            await interaction.followup.send(
                content=f'🚩 Banner for role {new_role.mention}', 
                view=view,
            )
            return
        await interaction.followup.send(
            content=f'Role {same_roles[0].name} is already exists\nRole id: {same_roles[0].id}', )

    @app_commands.command(name = "detector", description = "Detect specified propery of channel memders")
    @app_commands.describe(name="Object to detect")
    async def x_detector(self, interaction : discord.Interaction, name: str):
        await interaction.response.defer()
        view = DetectorButtons(name)
        await interaction.followup.send(
            content=f'{name} detector', 
            view=view,
        )




