from datetime import datetime
from email.mime import message
import discord
from discord import Sticker, app_commands
from discord.app_commands import Choice
from discord.ext import commands
from tinydb import Query

from modules.RawCommands import RawCommands
from modules.db_connector import db, memes, stickers

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

    @app_commands.command(name = "add_sticker", description = "Create new sticker")
    @app_commands.describe(sticker_name = "Name fo new sticker", image = "Link to sticker image",  )
    async def add_sticker(self, interaction : discord.Interaction, sticker_name : str, image: str, ):
        if stickers.get(Query().name == sticker_name):
            return await interaction.response.send_message(
                f'Sticker with name **{sticker_name}** already exists', ephemeral=True)
        new_sticker = dict(
            name=sticker_name, 
            image=image, 
            creation_date=str(datetime.now()),
        )
        quantity = stickers.insert(new_sticker)
        await interaction.response.send_message(f'Sticker added\n{new_sticker}', ephemeral=True)

    async def autocomplete_stickers(self, interaction: discord.Interaction, current: str):
        return [
            Choice(name = i['name'], value = i['name']) 
            for i in stickers.search(Query().name.exists())
        ]

    @app_commands.command(name = "sticker", description = "Send a sticker")
    @app_commands.describe(sticker_name = "Sticker name")
    @app_commands.autocomplete(sticker_name = autocomplete_stickers)
    async def send_sticker(self, interaction : discord.Interaction, sticker_name : str):
        image = stickers.get(Query().name == sticker_name)['image']
        await interaction.response.send_message(content=image)

    @app_commands.command(name = "sticker_info", description = "Get info about a sticker")
    @app_commands.describe(sticker_name = "Sticker name")
    @app_commands.autocomplete(sticker_name = autocomplete_stickers)
    async def sticker_info(self, interaction : discord.Interaction, sticker_name : str):
        sticker = stickers.get(Query().name == sticker_name)
        message = ''.join([f'{k}: {v}\n'for k, v in sticker.items()])
        await interaction.response.send_message(content=message)

    # TODO : add delete sticker command

