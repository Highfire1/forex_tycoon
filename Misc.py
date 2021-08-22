import discord
import os
import asyncio
from datetime import datetime
import discord.ext
from discord.ext import commands

from Player import Player, player_exists


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # print player balance and holdings
    @commands.command()
    async def profile(self, ctx):

        if player_exists(ctx.author.id) == False: # tell player to register
            await make_an_account(ctx)
            return

        user=ctx.author
        memberAvatar= user.avatar_url
        
        pl = Player(ctx.author.id)
        # TODO check player has account before all commands

        # create profile embed
        em = discord.Embed(title = "Profile", description = "", color = ctx.author.color)
        em.add_field(name='Balance', value="$" + str(pl.balance/100), inline=True)
        # TODO: make this look ok
        em.add_field(name='Holdings', value=pl.holdings, inline=True)
        em.set_thumbnail(url=memberAvatar)
        
        await ctx.reply(embed = em)  


    # register player
    # aka, generate a file for the player 
    # and give them some introduction
    # TODO: add an actual introduction to the bot
    @commands.command()
    async def register(self, ctx):
        if player_exists(ctx.author.id):
            await ctx.reply("You are already registered!")
            return

        pl = Player(ctx.author.id)
        pl.save()
        user=ctx.author
        memberAvatar= user.avatar_url

        em = discord.Embed(title = user, description = "", color = user.color)
        
        em.add_field(name="Welcome!", value='Welcome to FOREX Trading!', inline=True)
        em.add_field(name="Check out some commands!", value='!profile, !buy_order', 
        inline=True)

        em.set_thumbnail(url=memberAvatar)
        
        await ctx.reply(embed = em) 


# generate income
# everyone gets $100 every minute so people can't go bankrupt 
# and also to keep people engaged
# TODO: do things to stock market
async def run_cycle():

    await give_money()

    # prevent timer from eventually desyncing
    dt = datetime.now()  # get current timestamp
    seconds = dt.timestamp() # timestamp in seconds
    secondsinmin = seconds % 60 # modulo to 60

    # reloop
    loop = asyncio.get_event_loop() 
    loop.call_later(60 - secondsinmin, lambda: asyncio.ensure_future(run_cycle()))

# give money to everyone :D
async def give_money():
    hourly_income = 10000 # last 2 digits are pennies

    for player in os.listdir("players/"):
        id = player.replace(".csv", "")
        pl = Player(id)
        pl.balance += hourly_income
        pl.save()

async def make_an_account(ctx):
    await ctx.reply("MAKE AN ACCOUNT YOU BOZO")