import discord
import os
import time
import random
import discord.ext
from discord.ext import commands

class Extra(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))


    @commands.command()
    async def list_orders_mockup(self, ctx):
        print("running mockup")
        user=ctx.author
        memberAvatar = user.avatar_url
        
        em = discord.Embed(title = "List Orders for WOOGLE", description = "", color = ctx.author.color)

        price = random.randint(100, 1000)
        txt = ""
        for x in range(10):
            id = random.randint(1000, 9999)
            buysell = "BUY" if random.randint(0,1) else "SELL"
            sharenum = random.randint(0, 10)
            price = random.randint(price-50, price+50)


            txt += f"\n{id}... : {buysell} {sharenum } @ ${float(price)}"

        txt = f"```{txt}```"

        mins = random.randint(0, 13)
        em.add_field(name=f'In the last {mins} minutes', value=txt, inline=True)

        em.set_thumbnail(url=memberAvatar)
        
        await ctx.reply(embed = em)  

    # generated using https://cog-creators.github.io/discord-embed-sandbox/
    @commands.command()
    async def buy_options_mockup(self, ctx):
        em=discord.Embed(title="Buying Options", description="It looks like it's your first time here! Options are a form of speculative trading where you purchase the *right* to purchase or sell a certain stock...")
        em.add_field(name="Please select a stock to continue.", value="(options: APPLE, WOOGLE, UMUZON)", inline=False)

        msg = await ctx.reply(embed=em)
        await msg.add_reaction("🇦")
        await msg.add_reaction("🇼")
        await msg.add_reaction("🇺")

    # also generated using https://cog-creators.github.io/discord-embed-sandbox/
    @commands.command()
    async def stock_market_mockup(self, ctx):
        embed=discord.Embed(title="FOREX Stock Market", description="321.45 (+2.4%)")
        embed.set_image(url="https://i.imgur.com/XyJmjIi.png")
        await ctx.send(embed=embed)