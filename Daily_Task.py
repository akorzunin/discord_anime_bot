from discord.ext import tasks, commands
from anime_picture import AnimePicture
from nasa_picture import NasaPicture

class DailyTask(commands.Cog):
    def __init__(self, bot):
        self.index = 0
        self.bot = bot
        self.printer.start()
        self.daily_waifu_channel_list = []
        self.daily_nasa_channel_list = []
        self.a = AnimePicture()
        self.n =NasaPicture()

    def cog_unload(self):
        self.printer.cancel()

    @commands.command(help='Starts a coroutine', aliases=['good_day'])
    async def follow_daily_waifu(self, ctx):
        self.daily_waifu_channel_list.append(ctx)
        await ctx.send('This text channel is successfully following daily waifu mailing.')

    @commands.command(help='Ends a coroutine', )
    async def unfollow_daily_waifu(self, ctx):
        # self.daily_waifu_channel_list.pop(self.daily_waifu_channel_list.index(ctx))
        self.daily_waifu_channel_list = []
        await ctx.send('This text channel is not gonna receive daily waifu mailing.')

    @commands.command(help='Starts a coroutine', )
    async def follow_daily_nasa(self, ctx):
        self.daily_nasa_channel_list.append(ctx)   
        # print(ctx) 
        await ctx.send('This text channel is successfully following daily NASA APOD mailing.')

    @commands.command(help='Ends a coroutine', )
    async def unfollow_daily_nasa(self, ctx):
        # self.daily_nasa_channel_list.pop(self.daily_nasa_channel_list.index(ctx))
        self.daily_nasa_channel_list = []
        await ctx.send('This text channel is not gonna receive daily NASA APOD mailing.')


# 60 * 60 * 24  seconds in day
    @tasks.loop(seconds=(60 * 60 * 24),)
    async def printer(self, ):
        #get data from nasa api
        url, title, explanation = self.n.get_url()
        try:
            # TODO refactor after w/ discord embeds
            # send daily waifu picture to all channels in list
            await self.daily_waifu_channel_list[0].send('Daily waifu picture:')
            await self.daily_waifu_channel_list[0].send(f'{self.a.get_url()}')            
        except IndexError: print('No channel found for daily waifu mailing')
        try:
            # send daily waifu picture to all channels in list
            await self.daily_nasa_channel_list[0].send('Daily picture from NASA:')
            await self.daily_nasa_channel_list[0].send(f'{title}')
            await self.daily_nasa_channel_list[0].send(f'{url}')
            await self.daily_nasa_channel_list[0].send(f'{explanation}')
        except: print('No channel found for daily NASA APOD mailing')

    @printer.before_loop
    async def before_printer(self):
        print('waiting...')
        await self.bot.wait_until_ready()