import json

# function to handle buy/sell orders
# because gosh darn it we are an EDUCATIONAL project we have
# to implement this properly
# its me from the future! it was not implemented properly

class Orders():
    def __init__(self, stock, orders = []):
        self.stock = stock
        self.orders = []

        # todo: load from file
        try:
            with open(f"stocks/{self.stock}_orders.json", "r") as fi:
                self.orders = json.loads(fi.read())
        except:
            print(f"Loading orders for {stock} failed...")

            
            self.orders = []

    def save(self):
        with open(f"stocks/{self.stock}_orders.json", "w") as fi:
            json.dump(self.orders, fi, ensure_ascii=False, indent=4)

    
    # syntax:
    # [stock, player_id, type, money count, share count]
    async def add_order(self, order, ctx):

        self.orders.append(order)
        await self.fulfill_orders(ctx)


    # Every time a buy/sell order is posted, check to see if any of them can be fulfilled
    async def fulfill_orders(self, ctx):

        if len(self.orders) <= 1:
            return

        lowest_price = self.orders[0]
        for order in self.orders:
            if order[2] != "sell":
                continue
            if order[3] < lowest_price[3]:
                lowest_price = order
        
        print("LOWEST PRICE:", lowest_price)
        
        # fullfill buy orders
        for order in self.orders:
            if order[2] != "buy":
                continue
            if order[3] < lowest_price[3]:
                print("match found")
