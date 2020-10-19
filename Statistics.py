import json
import os
from multiprocessing import Pool
from random import random
from time import sleep

import Parameters


def generatestatistics(engine, history, signals, algorithm):

    comboparams = Parameters.loadparameters()
    groups = Parameters.generategroups(comboparams, history,signals,algorithm)

    # start 4 worker processes
    with Pool(processes=os.cpu_count()*2) as pool:
        processses = pool.starmap_async(calculatestatistic, groups,
                                        ).get()

        print(processses)
    print('PoolClosed?')

    # pool.terminate()
    # multiple_results = [pool.apply_async(Statistics.generatestatistics_2, (self.callback)) for i in range(10)]
    # [res.get() for res in multiple_results]

    # p = Process(target=Statistics.generatestatistics,
    #            args=(self.history, self.signals, self.algorithm, self.onstatisticscomplete))
    # p.start()
    # p.join()


def calculatestatistic(params, history, signals, algorithm):
    # print(history)
    # print(signals)
    # print(algorithm)
    print(f'Starto Processo with params: {params}')

    tradesActive = []

    #per ogni segnale
    for signal in signals:

        i = 0
        #trovo candela?
        for pos in history[signal.pair][signal.candle.tf]:
            if pos.date == signal.candle.date:
                break
            i+=1

        tp,sl = algorithm.processsignal(params, history[signal.pair][signal.candle.tf][i:], signal)


    sleep(5)
    print(f'Fine Processo!')
