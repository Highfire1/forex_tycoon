'''
Forex Tycoon: The discord stock market game!
Created by [insert names here]
'''



import discord
import os
from discord.ext import commands

from Stocks import Stock_Interface
from Mockups import Extra
from Misc import Info, run_cycle


# example on how to use player class
#bob = Player("213373983754551296")
#bob.save()
#print(bob.id)
#print(bob.balance)
#print(bob.holdings)

#stock = Stock("apple")
#stock.save()


# setup the bot
client = commands.Bot(
    case_insensitive=True,
    command_prefix="!")
client.remove_command("help")

#ready
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Forex Tycoon'))
    print('bot is ready~')
    
    # income loop
    await run_cycle()

#custom help
@client.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title = "Help", description = "Use !help <command> for extended information on a command.", color = ctx.author.color)
    #ex. em.add_field(name = "Moderation", value = "kick, ban, unban, clear")
    em.add_field(name = "Info", value = "profile, register")
    await ctx.reply(embed = em)

@help.command()
async def profile(ctx):
    em = discord.Embed(title = "profile", description = "Gives the profile of the user", color = ctx.author.color)

    em.add_field(name = "**Syntax**", value = "!profile")

    await ctx.reply(embed = em)  

@help.command()
async def register(ctx):
    em = discord.Embed(title = "register", description = "Registers a member into our lovely system", color = ctx.author.color)

    em.add_field(name = "**Syntax**", value = "!register")

    await ctx.reply(embed = em)  

#end of custom help


#command error
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found")


# overriding on_message example
@client.event
async def on_message(message):
    # don't scan messages sent by bots
    if message.author.bot:
        return
    # just for debug
    print("new message:", message.content)

    # required to make other commands still work
    await client.process_commands(message)


# add cogs
client.add_cog(Extra(client))
client.add_cog(Info(client))
client.add_cog(Stock_Interface(client))

# run bot
client.run(os.environ["token"])
