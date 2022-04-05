from .Base import Base
import numpy as np


class BarCountage(Base):

    def __init__(self) -> None:
        super().__init__()
        self.count = 0

    def loop(self, row):
        if not np.isnan(row["leg_start"]):
            if not np.isnan(row["leg_end"]) and self.leg_start_idx == row["leg_end"]:
                self.leg_start_idx = row["leg_start"]
                tmp = self.count+1
                self.count = 1
                return tmp

            self.leg_start_idx = row["leg_start"]

        if self.leg_start_idx != None:
            self.count += 1

        if not np.isnan(row["leg_end"]) and self.leg_start_idx == row["leg_end"]:
            tmp = self.count
            self.count = 0
            return tmp

    def run(self, _data):
        return _data.apply(lambda row: self.loop(row), axis=1)


class BarCountage2(Base):

    def __init__(self) -> None:
        super().__init__()

    def run(self, leg):
        return len(leg)
