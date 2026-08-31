class DayValues:

    def __init__(self, date, open_price, high_price, low_price, close_price, ema25 = 0, ema50 = 0):
        self.date = date
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.ema25 = ema25
        self.ema50 = ema50

    def __str__(self):
        return f"Day: {self.date}, open: {self.open_price}, high: {self.high_price}, low: {self.low_price} close: {self.close_price}"