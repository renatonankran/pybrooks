import numpy as np
import pandas as pd
from .zigzag import zz_direction
from .bars import bar_direction


class FindLegEnd():
    def __init__(self) -> None:
        self.leg_start = None
        self.zz_dir = 0
        self.old_dir = 0

    def loop(self, row):
        if not np.isnan(row['leg_start']):
            self.zz_dir = row['zz_direction']
            bar_dir = bar_direction(row)

            if self.leg_start != row["leg_start"]:
                tmp = self.leg_start
                self.leg_start = row["leg_start"]
                return tmp

            if self.zz_dir != 0 and self.zz_dir != bar_dir:
                return self.leg_start
            return np.nan

        if self.leg_start != None and not np.isnan(row['zz']):
            tmp = self.leg_start
            self.leg_start = None
            return tmp

    def run(self, _data):
        return _data.apply(lambda row: self.loop(row), axis=1)
