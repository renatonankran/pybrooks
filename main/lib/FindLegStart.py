from . import bars
import numpy as np
import pandas as pd
from .zigzag import zz_direction


class FindLegStart():
    def __init__(self) -> None:
        self.leg_start_direction = 0
        self.leg_counter = 0
        self.bar_returned = False
        self.nan_counter = 0
        self.old_direction = 0

    def leg_start(self, row):
        bar_dir = bars.bar_direction(row)

        if not np.isnan(row['zz']):
            self.old_direction = self.leg_start_direction
            self.leg_start_direction = zz_direction(row)
            if self.leg_counter != 0 and not self.bar_returned and bar_dir != 0:
                self.leg_counter += 1
                self.bar_returned = False
                return self.leg_counter, self.old_direction
            self.bar_returned = False

        if self.leg_start_direction != 0 and (bar_dir == self.leg_start_direction or bar_dir == 0):
            self.leg_counter += 1
            dir_tmp = self.leg_start_direction
            self.leg_start_direction = 0
            self.bar_counter = 0
            self.nan_counter = 0
            self.bar_returned = True
            return self.leg_counter, dir_tmp

        return np.nan, np.nan

    def run(self, _data):
        res = _data.apply(lambda row: self.leg_start(row), axis=1)
        return pd.DataFrame(res.tolist(), columns=["leg_start", "zz_direction"])
        # pd.DataFrame(res, columns=["leg_start", "zz_direction"])
