import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from datetime import datetime
from tinydb import Query

from modules.db_connector import stickers

class StickerSlashCommands(commands.Cog): 
    '''docstring for StickerSlashCommands'''
    def __init__(self, bot):
        self.bot = bot

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