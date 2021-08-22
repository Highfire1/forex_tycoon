from Orders import Orders

class Globals():
    stocks = ["apple", "woogle"]
    orders = {}

    for stock in stocks:
        orders[stock] = Orders(stock)