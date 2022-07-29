import asyncio
import logging
import requests
import random

import discord
#load .env variables

from modules.anime_picture import AnimePicture
from static_data.categories_list import categories, nsfw_categories

from datetime import datetime
from time import sleep

from discord.ext import commands

class AnimePic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.MSG_DELAY = 1
        self.a = AnimePicture()
    @commands.command()
    async def get_str(self, ctx, *args, **kwargs):
        logging.debug(args)
        await ctx.send('OK')
    @commands.command(aliases=['al'])
    async def azure(self, ctx, *args, **kwargs):
        '''Azure command return random picture with no args, avaliable args are: id {int}, name {str}'''        
        s = self.a.get_azure(args)
        if s == 0: 
            await ctx.send('Not found')
            return
        for i in s:
            await ctx.send(i['image'])
    @commands.command(aliases=['al_list'])
    async def azure_list(self, ctx, *args, **kwargs):
        '''Azure list of ids and names'''
        url = 'https://azurlane.koumakan.jp/wiki/List_of_Ships'
        await ctx.send(url)

    @commands.command(help='{category}(see list w/ >gc), {amount}(max 30) Shows anime picture(s) with waifu',aliases=['gw'])
    async def get_waifu(self, ctx, *args):
        def handle_args(args):
            get_random_category = lambda: 'waifu'
            # if first argument exist
            try:
                nt = args[0]
            except IndexError:
                category = get_random_category()
                amount = 1
                return category, amount
            try:
                pog = int(nt)
            except ValueError: pog = str(nt)
            # check if first argument is integer
            if isinstance(pog, int): 
                category = get_random_category()
                amount = pog
                return category, amount
            # if second argument exist
            try: 
                nt2 = args[1]
            except IndexError:
                # if there is no second argument 
                category = args[0]
                amount = 1
                return category, amount
            # if second argument is integer
            try:
                pog = int(nt2)
            except ValueError: pog = str(nt2)
            if isinstance(pog, int): 
                category = args[0]
                amount = pog
                return category, amount
        category, amount = handle_args(args)

        logging.debug(f'{category=}, {amount=}')
        if (amount != None) and (category != None):
            data = self.a.get_urls(amount, category=category)
            for i in data:
                await ctx.send(i)
                sleep(self.MSG_DELAY) # change to async sleep
        else: 
            data = self.a.get_url(category)
            await ctx.send(data)

    @commands.command(help='Shows avaliable categories' , aliases=['gc'])
    async def get_categories(self, ctx):

        await ctx.send(categories)