import itertools
import json
from itertools import permutations

from numpy.ma import arange, array


def loadparameters():

    jsonfile = open('Parameters.json', 'r', encoding='UTF-8')
    parameters = json.load(jsonfile)

    params = parameters['PARAMETERS']
    listparams = []

    for par in params:
        step = float(par['Step'])
        min = float(par['Minimum'])
        max = float(par['Maximum']) + step

        values = arange(min, max, step)
        listparams.append(values)

    # combinations = list(permutations(listparams, len(params)))
    combinations = list(itertools.product(*listparams))

    return combinations


def generategroups(comboparams, history, signals, algorithm):
    groups = []

    for combo in comboparams:
        groups.append((combo, history, signals, algorithm))

    return  groups