from Candle import Candle


class Consolidator:

    def __init__(self, pair: str, timeframe, callback):
        self.pair = pair
        self.tf = timeframe
        self.callback = callback

        self.candleserie = []

    def addcandle(self, candle: Candle):

        # arriva una nuova candela quindi devo processare il fatto se è consecutiva a quelle che ho gia o meno
        # per adesso proviamo ad unirle e basta

        self.candleserie.append(candle)

        if len(self.candleserie) >= self.tf:
            conscandle = Candle()
            conscandle.generate(self.candleserie)
            conscandle.generate(candle)






