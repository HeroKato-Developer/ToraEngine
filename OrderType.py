from enum import IntEnum


class OrderType(IntEnum):
    Buy = 0
    Sell = 1
    BuyOrder = 2
    SellOrder = 3
    BuyLimit = 4
    SellLimit = 5
