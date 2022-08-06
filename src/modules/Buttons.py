import random
import discord
from discord.ui import View

class BannerButtons(View):
    def __init__(self, role: discord.Role):
        super().__init__()
        self.role = role

    @discord.ui.button(
        label = "Get role", 
        style = discord.ButtonStyle.green, 
    )
    async def get_role(self, interaction:discord.Interaction, button: discord.ui.Button):
        '''Give new role to user if he dont have it'''
        if self.role not in interaction.user.roles:
            await interaction.user.add_roles(self.role)
            await interaction.response.send_message(content = f"You get role {self.role.name}")
            return
        await interaction.response.send_message(
            content = f"You already have role {self.role.name}", 
            ephemeral=True)

    @discord.ui.button(
        label = "Ping role", 
        style = discord.ButtonStyle.blurple, 
        emoji = "🔔",
    )
    async def ping_role(self, interaction:discord.Interaction, button: discord.ui.Button):
        '''Delete role from user'''
        if self.role in interaction.user.roles:
            await interaction.response.send_message(
                content = f"{self.role.mention} Get in here!")
            return
        await interaction.response.send_message(
            content = f"You don't have role {self.role.mention}",
            ephemeral=True)

    @discord.ui.button(
        label = "Remove role", 
        style = discord.ButtonStyle.red, 
    )
    async def del_role(self, interaction:discord.Interaction, button: discord.ui.Button):
        '''Delete role from user'''
        await interaction.user.remove_roles(self.role)
        await interaction.response.send_message(
            content = f"Role {self.role.name} removed!", ephemeral=True)


class DetectorButtons(View):
    def __init__(self, item: str):
        super().__init__()
        self.item = item

    @discord.ui.button(
        label = "Check me", 
        style = discord.ButtonStyle.green, 
    )
    async def check_user(self, interaction:discord.Interaction, button: discord.ui.Button):
        '''Give new role to user if he dont have it'''
        if bool(random.getrandbits(1)):
            await interaction.response.send_message(
                content = f"You are {self.item}", 
                ephemeral=True)
            await interaction.followup.send(
                content = f"{self.item} found!\nIt's {interaction.user.mention}", )
            return
        await interaction.response.send_message(
            content = f"You are not {self.item}", 
            ephemeral=True)
