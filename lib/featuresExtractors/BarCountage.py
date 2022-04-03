import Base
import numpy as np


class bar_countage(Base):

    def __init__(self) -> None:
        super().__init__()
        self.count = np.nan

    def loop(self, row):
        if self.leg_end(row):
            l_start_tmp = self.leg_start_idx
            self.leg_start_idx = None
            self.count = row.name-l_start_tmp+1

        if self.leg_start(row):
            self.leg_start_idx = row.name

        return self.result()

    def result(self):
        tmp = self.count
        self.count = np.nan
        return tmp
