import logging
import pickle
import asyncio
from datetime import datetime
import pytz
from discord import utils
from discord import Embed
from discord import Colour
from discord.ext import tasks, commands
from anime_picture import AnimePicture
from nasa_picture import NasaPicture

#load .env variables
import os
from dotenv import load_dotenv
load_dotenv()
PWD = os.getenv('PWD')

class DailyTask(commands.Cog):
    def __init__(self, bot):
        self.index = 0
        self.bot = bot
        self.printer_waifu.start()
        self.printer_nasa.start()

        self.a = AnimePicture()
        self.n =NasaPicture()

        self.daily_waifu_channel_id_list = self.get_list_from_file('daily_waifu')
        self.daily_nasa_channel_id_list = self.get_list_from_file('daily_nasa')
        logging.debug(self.daily_waifu_channel_id_list)
        logging.debug(self.daily_nasa_channel_id_list)
        # time zone
        self.tzdata = pytz.timezone('Europe/Moscow') 
        # init triggers at 6:00 by default
        self.trigger_time_waifu = self.tzdata\
            .localize(
                datetime.now()\
                    .replace(
                        hour=6, 
                        minute=0,
                        second=0,
                        microsecond=0
                    )
            )
        self.trigger_time_nasa = self.tzdata\
            .localize(
                datetime.now()\
                    .replace(
                        hour=6, 
                        minute=0,
                        second=0,
                        microsecond=0
                    )  
            ) 

    def cog_unload(self):
        self.printer_waifu.cancel()
        self.printer_nasa.cancel()
    
    def clear_list(self, filename):
        with open(PWD+f'\\static_data\\{filename}.pkl', 'wb') as f:
            pickle.dump([], f)

    def write_list_to_file(self, list_, filename):
        with open(PWD+f'\\static_data\\{filename}.pkl', 'wb') as f:
            pickle.dump(set(list_), f)

    def get_list_from_file(self, filename) -> list:
        try:
            with open(PWD+f'\\static_data\\{filename}.pkl', 'rb') as f:
                list_ = list(pickle.load(f))
        except FileNotFoundError: 
            self.clear_list(filename)
            return []
        return list_

    @commands.command(help='clear coroutine schedule', )
    async def unfollow_all(self, ctx):
        # save empty list to file
        self.clear_list('daily_waifu')
        self.clear_list('daily_nasa')
        # reload list from file
        self.daily_waifu_channel_id_list = self.get_list_from_file('daily_waifu')
        self.daily_nasa_channel_id_list = self.get_list_from_file('daily_nasa')
        await ctx.send('No more following.')

    @commands.command(help='Starts a coroutine', )
    async def follow_daily_waifu(self, ctx):
        self.daily_waifu_channel_id_list.append(ctx.channel.id)
        self.daily_waifu_channel_id_list = list(set(self.daily_waifu_channel_id_list))
        # save to file
        self.write_list_to_file(
            list_=self.daily_waifu_channel_id_list,
            filename='daily_waifu',
        )
        await ctx.send('This text channel is successfully following daily waifu mailing.')

    @commands.command(help='Ends a coroutine', )
    async def unfollow_daily_waifu(self, ctx):
        self.daily_waifu_channel_id_list.pop(self.daily_waifu_channel_id_list.index(ctx.channel.id))
        # save new list to file
        self.write_list_to_file(
            list_=self.daily_waifu_channel_id_list,
            filename='daily_waifu',
        )
        await ctx.send('This text channel is not gonna receive daily waifu mailing.')

    @commands.command(help='Starts a coroutine', )
    async def follow_daily_nasa(self, ctx):
        self.daily_nasa_channel_id_list.append(ctx.channel.id)
        self.daily_nasa_channel_id_list = list(set(self.daily_nasa_channel_id_list))
        # save to file 
        self.write_list_to_file(
            list_=self.daily_nasa_channel_id_list,
            filename='daily_nasa',
        )         
        await ctx.send('This text channel is successfully following daily NASA APOD mailing.')

    @commands.command(help='Ends a coroutine', )
    async def unfollow_daily_nasa(self, ctx):
        self.daily_nasa_channel_id_list.pop(self.daily_nasa_channel_id_list.index(ctx.channel.id))
        # save new list to file
        self.write_list_to_file(
            list_=self.daily_nasa_channel_id_list,
            filename='daily_nasa',
        )
        await ctx.send('This text channel is not gonna receive daily NASA APOD mailing.')

    @commands.command(help='Set time for coroutine', )
    async def set_time_daily_waifu(self, ctx, hours, minutes):
        logging.info(f'{hours}:{minutes}')
        self.trigger_time_waifu = self.tzdata\
            .localize(
                datetime.now().replace(
                    hour=int(hours), 
                    minute=int(minutes),
                    second=0,
                    microsecond=0
                )
            )
        td = self.trigger_time_waifu - datetime.now(self.tzdata)
        if td.total_seconds() < 0:
            self.trigger_time_waifu = self.trigger_time_waifu\
                                        .replace(day=self.trigger_time_waifu.day+1)
        await ctx.send(f'Next call time: {self.trigger_time_waifu}')
        await ctx.send(f'Time delta: {self.trigger_time_waifu - datetime.now(self.tzdata)}')

    @commands.command(help='Set time for coroutine', )
    async def set_time_daily_nasa(self, ctx, hours, minutes):
        logging.info(f'{hours}:{minutes}')
        self.trigger_time_nasa = self.tzdata\
            .localize(
                datetime.now().replace(
                    hour=int(hours), 
                    minute=int(minutes),
                    second=0,
                    microsecond=0
                )
            )
        td = self.trigger_time_nasa - datetime.now(self.tzdata)
        if td.total_seconds() < 0:
            self.trigger_time_nasa = self.trigger_time_nasa\
                                        .replace(day=self.trigger_time_nasa.day+1)
        await ctx.send(f'Next call time: {self.trigger_time_nasa}')
        await ctx.send(f'Time delta: {self.trigger_time_nasa - datetime.now(self.tzdata)}')
    
    @commands.command(help='Get time to coroutine', )
    async def get_time_daily_waifu(self, ctx,):
        await ctx.send(f'Time delta: {self.trigger_time_waifu - datetime.now(self.tzdata)}')

    @commands.command(help='Get time to coroutine', )
    async def get_time_daily_nasa(self, ctx,):
        await ctx.send(f'Time delta: {self.trigger_time_nasa - datetime.now(self.tzdata)}')


# 60 * 60 * 24  seconds in day
    #loop for daily waifu mailing
    @tasks.loop(seconds=(60 * 60 * 24),)
    async def printer_waifu(self, ):
        await utils.sleep_until(self.trigger_time_waifu)
        self.trigger_time_waifu = self.trigger_time_waifu.replace(day=self.trigger_time_waifu.day+1)
        url = self.a.get_url()
        embed = Embed(
            title='Daily waifu picture:',
            colour=Colour.blue(),
            url=url,
        )
        embed.set_image(url=url)
        for channel_id in self.daily_waifu_channel_id_list:
            channel = self.bot.get_channel(channel_id)
            await channel.send(embed=embed)

    #loop for daily nasa mailing
    @tasks.loop(seconds=(60),)
    async def printer_nasa(self, ):
        await utils.sleep_until(self.trigger_time_nasa)
        self.trigger_time_nasa = self.trigger_time_nasa.replace(day=self.trigger_time_nasa.day+1)
        url, title, explanation, stat, stat_value = self.n.get_url()
        embed = Embed(
            title=title,
            description=explanation,
            colour=Colour.blue(),
            url=url,
        )
        embed.set_image(url=url)
        embed.set_footer(text=f"{stat}\n{stat_value}",)
        for channel_id in self.daily_nasa_channel_id_list:
            channel = self.bot.get_channel(channel_id)
            await channel.send(embed=embed)


    @printer_waifu.before_loop
    async def before_printer(self):
        logging.info('waiting...')
        await self.bot.wait_until_ready()

    @printer_nasa.before_loop
    async def before_printer(self):
        logging.info('waiting...')
        await self.bot.wait_until_ready()
        # mb change or extend this await till certain time  (12 am)