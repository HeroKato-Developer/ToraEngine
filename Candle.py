import datetime
from decimal import Decimal


class Candle:

    def __init__(self):
        self.pair = ''
        self.date = None
        self.dateend = None
        self.open = 0
        self.high = 0
        self.low = 0
        self.close = 0
        self.size = 0
        self.tf = 0

    def set(self, pair, date, open, high, low, close, size):
        self.pair = pair
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
        self.pair = serie[first].pair
        self.date = serie[first].date
        self.dateend = serie[last].date + datetime.timedelta(seconds=60)
        self.open = 0
        self.high = 0
        self.low = 0
        self.close = 0
        self.size = 0

        # first pass per settare valori high low e open
        for candle in serie:
            if candle.isvalid():
                self.open = candle.open
                self.high = candle.high
                self.low = candle.low
                break

        # second pass per settare close
        for candle in reversed(serie):
            if candle.isvalid():
                self.close = candle.close
                break

        # third pass per settare high low
        for candle in serie:
            if not candle.isvalid():
                continue

            if candle.high > self.high:
                self.high = candle.high

            if candle.low < self.low:
                self.low = candle.low

            # aggiungo size della candela
            self.size += candle.size

    def checkiflist(self, candles):
        if type(candles) is list:
            return candles
        else:
            return [candles]

    def isvalid(self):
        if self.open == 0 and self.high == 0 and self.low == 0 and self.close == 0:
            return False
        return True

    def tostring(self):
        return f'Candle: From{self.date} To:{self.dateend} - TF:{self.tf} - O:{self.open} - H:{self.high} - L:{self.low} - C:{self.close}'
