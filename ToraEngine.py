import datetime
import Utilities
from Algorithm import Algorithm
from Consolidator import Consolidator
from DataReader import DataReader
from DataReaderFxcm import DataReaderFxcm


class ToraEngine:

    def __init__(self):
        self.ready = False

        self.datareader = None
        self.history = []
        self.consolidators = {}
        self.algorithm = None
        self.pairs = []

        self.datecurrent = None
        self.datestart = None
        self.dateend = None
        self.initialize()

    def initialize(self):
        self.datareader = DataReaderFxcm()

    def addalgorithm(self, algo: Algorithm):
        self.algorithm = algo(self)

    def addconsolidator(self, pair, timeframe, callback):

        pair = pair.lower()

        if pair not in self.pairs:
            self.pairs.append(pair)

        if len(self.consolidators) == 0:
            self.consolidators.setdefault(pair, [])

        self.consolidators[pair].append(Consolidator(pair, timeframe, callback))

    def setcomputingdates(self, start: datetime, end: datetime):
        self.datestart = Utilities.stringtotime(start)
        self.dateend = Utilities.stringtotime(end)
        self.datecurrent = self.datestart

        print(
            f'Set Start Date: {start} - Year: {self.datestart.year} - Month: {self.datestart.month} - Day: {self.datestart.day}\nSet End Date: {end} - Year: {self.dateend.year} - Month: {self.dateend.month} - Day: {self.dateend.day}')

    def run(self):
        # carico tutte le candele ?
        self.datareader.loadhistory(self.consolidators, self.datestart, self.dateend)

        while self.datecurrent < self.dateend:
            self.consolidate()

    def consolidate(self):
        for pair in self.pairs:
            candle = self.datareader.readnext(self.datecurrent, pair)

            for consolidator in self.consolidators[pair]:
                consolidator.addcandle(candle)

        self.datecurrent += datetime.timedelta(0, 60)


# creo engine
Engine = ToraEngine()

# aggiungo algoritmo
Engine.addalgorithm(Algorithm)

# runno
Engine.run()

# aggiungo algoritmo
# aggiungo outputs

# fine
