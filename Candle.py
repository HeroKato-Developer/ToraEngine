class Candle:

    def __init__(self):
        self.date = None
        self.open = 0
        self.high = 0
        self.low = 0
        self.close = 0
        self.size = 0

    def set(self, date, open, high, low, close, size):
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.size = size

    def generate(self, candles):
        serie = self.checkiflist(candles)

    def checkiflist(self, candles):
        if type(candles) is list:
            return candles
        else:
            return list(candles)
