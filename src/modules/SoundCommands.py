import asyncio
from datetime import datetime
import logging
from tinydb import Query
import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice

from modules.RawSoundCommands import RawSoundCommands
from modules.db_connector import sounds


class SoundCommads(commands.Cog, RawSoundCommands): 
    '''docstring for SoundCommads'''
    def __init__(self, bot, sound):
        self.bot = bot
        self.sound = sound

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""
        await self.play_command(ctx, query)
        await ctx.send(f'Now playing: {query}')

    # TODO add some decorators to clean up code /get_ctx /bebofe_slash /after_slash
    @app_commands.command(name = "play", description = "Play a sound from url or query")
    @app_commands.describe(query = "Query or url")
    async def slash_play(self, interaction : discord.Interaction, query: str):
        ctx = await self.get_ctx(interaction)
        await self.sound._ensure_voice(ctx)
        await self.play_command(ctx, query)
        await interaction.followup.send(content=f'Now playing: {query}')
        await self.sound._leave_voice(ctx)

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""
        player = await self.stream_command(ctx, url)
        await ctx.send(f'Now playing: {player.title}')

    @app_commands.command(name = "stream", description = "Stream a sound from url or query")
    @app_commands.describe(url = "url or query")
    async def slash_stream(self, interaction : discord.Interaction, url: str):
        ctx = await self.get_ctx(interaction)
        await self.sound._ensure_voice(ctx)
        await self.stream_command(ctx, url)
        await interaction.followup.send(content=f'Now playing: {url}')
        await self.sound._leave_voice(ctx)

    @commands.command(aliases=['vol'])
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""
        await self.volume_command(ctx, volume)
        await ctx.send(f"Changed volume to {volume}%")

    @app_commands.command(name='volume', description='Set a volume while bot is playing')
    @app_commands.describe(volume='volume')
    async def slash_volume(self, interaction: discord.Interaction, volume: int):
        ctx = await self.get_ctx(interaction)
        await self.volume_command(ctx, volume)
        await interaction.followup.send(content=f"Changed volume to {volume}%")

    @commands.command(aliases= ['dv', 'defvol'])
    async def set_default_volume(self, ctx, volume: int):
        """Changes the player's volume"""
        self.sound.default_volume = volume
        await ctx.send(f"Changed default volume to {volume}%")

    @app_commands.command(name='set_default_volume', description='Set default volume to a BotSlashCommands')
    @app_commands.describe(volume='default_volume')
    async def slash_set_default_volume(self, interaction: discord.Interaction, volume: int):
        self.sound.default_volume = volume
        await interaction.response.send_message(f"Changed default volume to {volume}%")

    @commands.command(aliases=['disconnect', 'leave'])
    async def close(self, ctx):
        """Stops and disconnects the bot from voice"""
        await ctx.voice_client.disconnect()

    @app_commands.command(name='leave', description='Leave from voie channel')
    async def slash_close(self, interaction: discord.Interaction, ):
        ctx = await self.get_ctx(interaction)
        await ctx.voice_client.disconnect()
        await interaction.response.send_message(content=f'Left channel: {ctx.author.voice.channel.name}')

    @commands.command()
    async def buffer(self, ctx, wait_time: int=5):
        """Bufferize stream (can take int [seconds])"""
        msg = await ctx.send('Buffering...')
        ctx.voice_client.pause()
        await asyncio.sleep(wait_time)
        ctx.voice_client.resume()
        await msg.edit(content='Done')
        # await ctx.send('Done')

    @commands.command(aliases=['halt'])
    async def stop(self, ctx):
        """Stops player"""
        ctx.voice_client.stop()
        await ctx.send('Stopped')

    @app_commands.command(name='stop', description='Stop plying')   
    async def slash_stop(self, interaction: discord.Interaction, ):
        ctx = await self.get_ctx(interaction)
        ctx.voice_client.stop()
        await interaction.response.send_message(content='Stopped')

    @commands.command()
    async def pause(self, ctx):
        """Pause player"""
        ctx.voice_client.pause()
        await ctx.send('Paused')

    @app_commands.command(name='pause', description='Pause plying, resumable')   
    async def slash_pause(self, interaction: discord.Interaction, ):
        ctx = await self.get_ctx(interaction)
        ctx.voice_client.pause()
        await interaction.response.send_message(content='Paused')

    @commands.command()
    async def resume(self, ctx):
        """Resume player"""
        ctx.voice_client.resume()
        await ctx.send('Resumed')

    @app_commands.command(name='resume', description='Resume plying')   
    async def slash_resume(self, interaction: discord.Interaction, ):
        ctx = await self.get_ctx(interaction)
        ctx.voice_client.resume()
        await interaction.response.send_message(content='Resumed')

    @commands.command(aliases=['mjoin'])
    async def manual_join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

    @commands.command()
    async def join(self, ctx):
        """Joins to sender voice channel"""
        await self.join_command(ctx)

    @app_commands.command(name='join', description='Join voice channel')
    async def slash_join(self, interaction: discord.Interaction, ):
        ctx = await self.get_ctx(interaction)
        await self.join_command(ctx)
        if ctx.author.voice:
            await interaction.response.send_message(content=f'Joined to channel: {ctx.author.voice.channel.name}')
            return
        await interaction.response.send_message(content='User not connected to voice channel')

    @commands.command(aliases=['gv'])
    async def get_volume(self, ctx, ):
        """Return current volume level"""
        await ctx.send(f"Current volume: {ctx.voice_client.source.volume*100}\nDefault volume: {self.sound.default_volume}")

    @play.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        await self.sound._ensure_voice(ctx)
    
    @play.after_invoke
    @stream.after_invoke
    async def leave_voice(self, ctx):
        await self.sound._leave_voice(ctx)

    ### Custom sounds

    @app_commands.command(name = "add_sound", description = "Create new sound")
    @app_commands.describe(sound_name = "Name fo new sound", url = "Link to sound",  )
    async def add_sound(self, interaction : discord.Interaction, sound_name : str, url: str, ):
        if sounds.get(Query().name == sound_name):
            return await interaction.response.send_message(
                f'sound with name **{sound_name}** already exists', ephemeral=True)
        new_sound = dict(
            name=sound_name, 
            url=url, 
            creation_date=str(datetime.now()),
        )
        quantity = sounds.insert(new_sound)
        await interaction.response.send_message(f'sound added\n{new_sound}', ephemeral=True)

    async def autocomplete_sounds(self, interaction: discord.Interaction, current: str):
        return [
            Choice(name = i['name'], value = i['name']) 
            for i in sounds.search(Query().name.exists())
        ]

    @app_commands.command(name = "sound", description = "Send a sound")
    @app_commands.describe(sound_name = "sound name")
    @app_commands.autocomplete(sound_name = autocomplete_sounds)
    async def send_sound(self, interaction : discord.Interaction, sound_name : str):
        # TODO fix empty sund err and in stickers too
        url = sounds.get(Query().name == sound_name)['url']
        ctx = await self.get_ctx(interaction)
        await self.sound._ensure_voice(ctx)
        await self.stream_command(ctx, url)
        await interaction.followup.send(content=f'Now playing: {url}')
        await self.sound._leave_voice(ctx)

    @app_commands.command(name = "sound_info", description = "Get info about a sound")
    @app_commands.describe(sound_name = "sound name")
    @app_commands.autocomplete(sound_name = autocomplete_sounds)
    async def sound_info(self, interaction : discord.Interaction, sound_name : str):
        sound = sounds.get(Query().name == sound_name)
        message = ''.join([f'{k}: {v}\n'for k, v in sound.items()])
        await interaction.response.send_message(content=message)
    
    # TODO delete sound