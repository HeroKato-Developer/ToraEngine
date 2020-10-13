import csv
import datetime
import time
from io import StringIO

import pandas as pd
from decimal import Decimal, getcontext
from unicodedata import decimal
from zipfile import ZipFile, BadZipFile

from numpy import NaN

from Candle import Candle
from ProgressBar import printProgressBar


class DataReader:

    def __init__(self):
        self.data = {}
        self.dataframe = pd.DataFrame()
        self.dataframes = []
        self.path = '../Polygon/Lean/Data/forex/fxcm/minute/'

    def loadhistory(self, consolidators, datestart: datetime.datetime, dateend: datetime.datetime):
        for pair in consolidators:
            # verifico che non ci sia gia in quelli caricati
            if pair in self.data:
                continue

            datadiff = dateend - datestart
            daystotal = datadiff.days
            dayscurrent = 0

            relpath = f'{self.path}{pair}/'

            # inizio il ciclo di caricamento partendo dall inizio
            datecurrent = datestart

            while datecurrent < dateend:
                self.loadfromzip(datecurrent, relpath, pair)
                datecurrent += datetime.timedelta(1)
                dayscurrent += 1
                printProgressBar(dayscurrent, daystotal, f'Loading {pair} History {datecurrent}: ')

            print(f'Merging DataFrame for {pair}')
            self.dataframe = self.dataframe.append(self.dataframes)
            self.dataframes = None
            print(f'Finished Merging DataFrame for {pair}')

            #for count in range(0, len(self.dataframes)):
            #    self.dataframe = self.dataframe.append(self.dataframes[count])

            #    if count % 10 == 0:
             #       printProgressBar(count, len(self.dataframes), f'Merging DataFrames: ')

    def loadfromzip(self, datecurrent: datetime, path: str, pair: str):

        file = self.generatepath(datecurrent, path)

        # carico il file del giorno e lo aggiungo
        try:
            with ZipFile(file, 'r') as zip:
                for zipfile in zip.namelist():
                    # print(f'Reading file in zip: {zipfile}')
                    datazip = zip.read(zipfile)
                    datalines = datazip.decode("utf-8")
                    # datalines = datalines.splitlines()

                    convert = lambda x: datecurrent + datetime.timedelta(milliseconds=int(x))
                    df = pd.read_csv(StringIO(datalines),
                                     header=None,
                                     index_col=0,
                                     names=['Time', 'Ob', 'Hb', 'Lb', 'Cb', 'Sb', 'Oa', 'Ha', 'La', 'Ca', 'Sa'],
                                     parse_dates=['Time'],
                                     date_parser=convert)

                    # print(df)

                    self.dataframes.append(df)
                    # self.dataframe = pd.concat([self.dataframe, df])

                    # csv_reader = csv.reader(datalines, delimiter=',')
                    # csv_parsed = list(csv_reader)

                    # csv_parsed è la lista di tutte le candele con i propri campi
                    # carico tutte le candele da m1
                    # self.loadminutes(csv_parsed, pair, datecurrent)

        except FileNotFoundError:
            # print(f'File Non Esistente - {file}')
            pass

        except BadZipFile:
            # print(f'Zip Errore, impossibile aprire')
            pass

    def readnext(self, date: datetime, pair: str):

        if date not in self.data[pair]:
            # print(f'Void Candle - Date {date} does NOT exist in {pair}')
            candle = Candle()
            candle.pair = pair
            candle.date = date
            return candle

        # recupero la candela
        return self.data[pair][date]

    def generatepath(self, datecurrent: datetime, path: str):
        return path + datecurrent.strftime('%Y%m%d') + '_quote.zip'

    def loadminutes(self, csv, pair, datecurrent: datetime):

        for row in csv:
            candle = self.loadcandle(row, pair, datecurrent)

            if pair not in self.data:
                self.data.setdefault(pair, {})
                self.data[pair].setdefault(candle.date, None)

            self.data[pair][candle.date] = candle

    def loadcandle(self, row, pair: str, datecurrent: datetime):

        # found in fxcm folder!
        # | Time | Bid Open | Bid High | Bid Low | Bid Close | Last Bid Size | Ask Open | Ask High | Ask Low | Ask Close | Last Ask Size |
        # |   0  |     1    |     2    |    3    |      4    |      5        |    6     |     7    |   8     |     9     |       10      |

        # Digits conversion
        # https://stackoverflow.com/questions/6189956/easy-way-of-finding-decimal-places
        digits = abs(Decimal(row[1]).as_tuple().exponent)

        # Digits precision
        # https://gist.github.com/jackiekazil/6201722
        getcontext().prec = digits + 1

        milliseconds = int(row[0])
        open = (Decimal(row[1]) + Decimal(row[6])) * Decimal('0.5')
        high = (Decimal(row[2]) + Decimal(row[7])) * Decimal('0.5')
        low = (Decimal(row[3]) + Decimal(row[8])) * Decimal('0.5')
        close = (Decimal(row[4]) + Decimal(row[9])) * Decimal('0.5')
        size = (Decimal(row[5]) + Decimal(row[10])) * Decimal('0.5')

        date = datecurrent + datetime.timedelta(0, 0, 0, milliseconds)
        # datestr = date.strftime('%Y-%m-%d %H:%M:%S')

        candle = Candle()
        candle.set(pair, date, open, high, low, close, size)

        # return candle to be added to history
        return candle

    def loadcandle_new(self, date, pair):
        relpath = f'{self.path}{pair}/'
        file = self.generatepath(date, relpath)

        # carico il file del giorno e lo aggiungo
        try:
            with ZipFile(file, 'r') as zip:
                for zipfile in zip.namelist():
                    # print(f'Reading file in zip: {zipfile}')
                    datazip = zip.read(zipfile)
                    datalines = datazip.decode("utf-8")
                    datalines = datalines.splitlines()

                    csv_reader = csv.reader(datalines, delimiter=',')
                    csv_parsed = list(csv_reader)

                    # csv_parsed è la lista di tutte le candele con i propri campi
                    # carico tutte le candele da m1
                    return self.loadminute_new(csv_parsed, pair, date)

        except FileNotFoundError:
            # print(f'File Non Esistente - {file}')
            pass

        except BadZipFile:
            # print(f'Zip Errore, impossibile aprire')
            pass

    def loadminute_new(self, csv, pair, date: datetime.datetime):

        datedefault = date.replace(hour=0, minute=0)

        for row in csv:

            if datedefault + datetime.timedelta(milliseconds=int(row[0])) != date:
                continue

            candle = self.loadcandle(row, pair, date)
            return candle
