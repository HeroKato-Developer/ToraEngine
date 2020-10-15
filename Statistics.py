from random import random
from time import sleep

def generatestatistics(count, history, signals, algorithm, callback):
    # print(history)
    # print(signals)
    # print(algorithm)
    print(f'Starto Processo: {count}')
    sleep(10)
    callback(f'Fine Processo: {count}')


def generatestatistics_2(count, callback):

    number = random() * 10
    print(f'Starto Processo: {number}')
    sleep(number)
    return callback(number)
    #print(f'Fine Processo: {count}')
