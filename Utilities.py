from datetime import datetime


def stringtotime(date):
    return datetime.strptime(date, '%Y/%m/%d')
