from Candle import Candle


class Consolidator:

    def __init__(self, pair: str, timeframe, callback):
        self.pair = pair
        self.tf = timeframe
        self.callback = callback

        self.candleserie = []
        self.candlecount = 0

    def addcandle(self, candle: Candle):

        # arriva una nuova candela quindi devo processare il fatto se è consecutiva a quelle che ho gia o meno
        # per adesso proviamo ad unirle e basta
        # -------------------------------------------------------------------------------------------

        # la aggiungo alla lista
        self.candleserie.append(candle)

        # verifico la data della candela
        if len(self.candleserie) >= self.tf:
            conscandle = Candle()
            conscandle.consolidate(self.candleserie, self.tf)

            #chiamo evento consolidate
            self.callback(conscandle)

    def processcandle(self):
        pass
