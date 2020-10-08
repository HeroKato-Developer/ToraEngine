from decimal import Decimal


class Candle:

    def __init__(self):
        self.date = None
        self.open = 0
        self.high = 0
        self.low = 0
        self.close = 0
        self.size = 0
        self.tf = 0

    def set(self, date, open, high, low, close, size):
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.size = size

    def consolidate(self, candles, timeframe):
        serie = self.checkiflist(candles)

        first = 0
        last = len(serie) - 1

        self.tf = timeframe
        self.date = serie[first].date
        self.open = serie[first].open
        self.close = serie[last].close

        # first pass per settare valori high low
        for candle in serie:
            if candle.isvalid():
                self.high = candle.high
                self.low = candle.low
                break

        # pass per settare high low
        for candle in serie:
            if not candle.isvalid():
                continue

            if candle.high > self.high:
                self.high = candle.high

            if candle.low < self.low:
                self.low = candle.low

    def checkiflist(self, candles):
        if type(candles) is list:
            return candles
        else:
            listcandles = [candles]
            return listcandles

    def isvalid(self):

        if self.open == 0 and self.high == 0 and self.low == 0 and self.close == 0:
            return False

        return True

    def tostring(self):

        return f'{self.date} - O:{self.open} - H:{self.high} - L:{self.low} - C:{self.close} - TF:{self.timeframe}'
