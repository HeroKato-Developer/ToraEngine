from Candle import Candle
from OrderType import OrderType
from TimeFrame import TimeFrame


class Algorithm:

    def __init__(self, engine):
        self.engine = engine
        self.countsignal = 0
        self.initialize()

    def initialize(self):
        self.engine.setcomputingdates('2019/10/29', '2019/11/01')
        self.engine.addconsolidator('EURUSD', TimeFrame.M15, self.onconsolidate)
        # self.engine.addconsolidator('USDJPY', TimeFrame.M15, self.onconsolidate)

    def onconsolidate(self, candle: Candle):
        # print(f'Event On Consolidate - {candle.tostring()}')

        self.countsignal += 1
        if self.countsignal >= 60:
            self.countsignal = 0
            self.engine.signal(OrderType.Buy, candle.pair, candle)

    def processsignal(self, parameters, history, signal):
        print(f'Generating TP and sl')
        return 0,0
