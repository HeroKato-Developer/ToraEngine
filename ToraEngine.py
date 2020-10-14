import datetime
import Utilities
from multiprocessing import Process
from Algorithm import Algorithm
from Candle import Candle
from Consolidator import Consolidator
from DataReaderFxcm import DataReaderFxcm
from ProgressBar import progressbar
from Signal import Signal
import Statistics
from TimeFrame import TimeFrame


class ToraEngine:

    def __init__(self):
        self.ready = False

        self.datareader = None
        self.history = {}
        self.consolidators = {}
        self.signals = []
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
            self.addrollingwindow(pair)

        if pair not in self.consolidators:
            self.consolidators.setdefault(pair, [])

        self.consolidators[pair].append(Consolidator(pair, timeframe, callback))

    def addtohistory(self, candle: Candle):
        # verifico se esiste il pair
        if candle.pair not in self.history:
            self.history.setdefault(candle.pair, {})

        # verifico se esiste il tf
        if candle.tf not in self.history[candle.pair]:
            self.history[candle.pair].setdefault(candle.tf, [])

        # aggiungo candela alla history
        self.history[candle.pair][candle.tf].insert(0, candle)

    def addrollingwindow(self, pair):

        for tf in TimeFrame:
            self.addconsolidator(pair, tf, self.addtohistory)

    def addsignal(self, signal: Signal):
        self.signals.insert(0, signal)

    def setcomputingdates(self, start: datetime, end: datetime):
        self.datestart = Utilities.stringtotime(start)
        self.dateend = Utilities.stringtotime(end)
        self.datecurrent = self.datestart

        print(
            f'Set Start Date: {start} - Year: {self.datestart.year} - Month: {self.datestart.month} - Day: {self.datestart.day}\nSet End Date: {end} - Year: {self.dateend.year} - Month: {self.dateend.month} - Day: {self.dateend.day}')

    def consolidate(self):
        for pair in self.pairs:
            candle = self.datareader.readnext(self.datecurrent, pair)

            for consolidator in self.consolidators[pair]:
                consolidator.addcandle(candle)

        self.datecurrent += datetime.timedelta(0, 60)

    def signal(self, type, pair, price, date):

        # creo un signal e lo aggiungo alla lista
        signal = Signal(type, pair, price, date)
        self.addsignal(signal)

    def start(self):
        # carico tutte le candele ?
        self.datareader.loadhistory(self.consolidators, self.datestart, self.dateend)

        dayscurrent = 0
        daystotal = self.dateend - self.datecurrent
        daystotal = daystotal.days

        while self.datecurrent < self.dateend:
            self.consolidate()

            dayscurrent = self.datecurrent - self.datestart
            dayscurrent = dayscurrent.days

            progressbar(dayscurrent, daystotal, 'Calculating Algorithm: ', f'Current Date: {self.datecurrent}')

        # creo processi che vanno a calcolare i segnali
        self.statistics()

    def statistics(self):
        p = Process(target=Statistics.generatestatistics,
                    args=(self.history, self.signals, self.algorithm, self.onstatisticscomplete))
        p.start()
        p.join()

    def onstatisticscomplete(self, var):
        print(var)
