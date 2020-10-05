from TimeFrame import TimeFrame


class Algorithm:

    def __init__(self, toraengine):
        self.engine = toraengine
        self.initialize()

    def initialize(self):
        print(f'Im an Algo!')

        self.engine.setcomputingdates('2019/08/02', '2020/01/02')
        self.engine.addconsolidator('EURUSD', TimeFrame.M1, self.onconsolidate)

    def onconsolidate(self):
        print('Event On Consolidate')
