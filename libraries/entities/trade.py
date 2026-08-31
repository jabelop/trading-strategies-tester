class Trade:

    def __init__(self, date, price, quantity, cost, type_t, coin):
        self.date = date
        self.price = price
        self.quantity = quantity
        self.cost = cost
        self.type_t = type_t
        self.coin = coin

    def __str__(self):
        return f"Day: {self.date}, price: {self.price}, quantity: {self.quantity}, cost: {self.cost} type_t: {self.type_t} coin: {self.coin}"
