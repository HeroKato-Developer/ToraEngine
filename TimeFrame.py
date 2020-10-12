from enum import IntEnum


class TimeFrame(IntEnum):
    M1 = 1
    M5 = 5
    M15 = 15
    M30 = 30
    H1 = 60
    H4 = 240
    D1 = 1440

    def __iter__(self):
        return [self.M1, self.M5, self.M15, self.M30, self.H1, self.H4, self.D1]
