import discord
import discord.ext
from discord.ext import commands

from Player import Player, player_exists
from Misc import make_an_account
from Globals import Globals

class Stock_Interface(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # display info for a stock
    # TODO change to getting info from class
    @commands.command()
    async def stock_info(self, ctx):
        if player_exists(ctx.author.id) == False: # tell player to register
            await make_an_account(ctx)
            return
            
        content = ctx.message.content.replace("!stock_info", "").strip()

        if content not in Globals.stocks: 
            await ctx.reply("Stock doesn't exist .-. Try one of these: ", Globals.stocks)
            return

        # TODO needs an embed
        
        st = Stock(content)
        # load prices of sellable stock into a dictionary
        stock_prices = {}
        for share in st.data:

            if share[1] == "None": 
                printvalue = int(share[2])/100
                if printvalue not in stock_prices:
                    stock_prices[printvalue] = 1
                else:
                    stock_prices[printvalue] += 1
        

        user=ctx.author
        em = discord.Embed(title = f'{content} stock', description = '', color = user.color)

        value = ""
        for price, key in sorted(stock_prices.items()):
            value += "\n" + str(key) + " shares : $" + str(price)

        if len(stock_prices) == 0:
            em.add_field(name="Sorry!", value = "Looks like there currently aren't any shares available!", inline = True)
        else:
            em.add_field(name="​Available shares: ", value=value, inline=True) 
        
        await ctx.reply(embed = em) 

    @commands.command()
    async def buy_order(self, ctx):
        await self.create_order(ctx, "buy")

    @commands.command()
    async def sell_order(self, ctx):
        await self.create_order(ctx, "sell")


    async def create_order(self, ctx, type_):

        if player_exists(ctx.author.id) == False: # tell player to register
            await make_an_account(ctx)
            return
    
        parameters = ctx.message.content.split(" ")

        if len(parameters) != 4:
            await ctx.reply("bad input")
            return
        
        
        # generate the order
        try:
            order = []
            order.append(parameters[1])      # 0 stock REQ
            order.append(ctx.author.id)      # 1 id OPT
            order.append(type_)              # 2 option type OPT
            order.append(int(parameters[2])) # 3 price per share REQ
            order.append(int(parameters[3])) # 4 share count REQ
        except:
            await ctx.reply("Sorry, something went wrong; check your parameters.")
            return

        # code for buying stock
        if order[2] == "buy":
            order_cost = order[3] * order[4]

            pl = Player(order[1])
            if pl.balance < order_cost:
                await ctx.reply(f"Insufficient Funds! You only have ${pl.balance}")
                return

            pl.balance -= order_cost

            # reply with confirmation
            s = "s" if int(order[4]) > 1 else ""
            await ctx.reply(f"Buying {order[4]} share{s} of {order[0]} stock!")
        
        # code for selling stock
        elif order[2] == "sell":
            # TODO: check if we own stock of that type
            # TODO: set status of stock to a sellingid

            # reply with confirmation
            s = "s" if int(order[4]) > 1 else ""
            await ctx.reply(f"Selling {order[4]} share{s} of {order[0]} stock!")


        # call the order handler
        await Globals.orders[order[0]].add_order(order, ctx)
        Globals.orders[order[0]].save()




class Stock():
    def __init__(self, stockname, data = []):
        self.stockname = stockname
        data = []

        # TODO load stock from file
        with open(f"stocks/{stockname}.csv", "r") as stockdata:
            stockdata.readline() # skip the header row

            for share in stockdata.readlines():
                data.append(share.strip().split(","))
            #print(data)
        
        self.data = data
    
    def save(self):
        with open(f"stocks/{self.stockname}.csv", "w") as stockdata:
            data = "stock_num,owner,list_price"
            for share in self.data:
                data += "\n" + ','.join(share)
            stockdata.write(data)
    



    


        
    
    
    
    # TODO function to update stock

    # TODO function to randomly buy/sell stocks
