
import numpy as np
from .. import bars


class DirectionalBarCount():

    def __init__(self) -> None:
        super().__init__()
        self.count = 0
        self.zz_dir = None
        self.leg_start_idx = None

    def loop(self, row):
        self.bar_dir = bars.bar_direction(row)
        if not np.isnan(row["leg_start"]):
            if not np.isnan(row["leg_end"]) and self.leg_start_idx == row["leg_end"]:
                self.leg_start_idx = row["leg_start"]
                self.zz_dir = row["zz_direction"]
                tmp = self.count
                self.count = 0
                if self.zz_dir != self.bar_dir:
                    tmp += 1
                if self.zz_dir == self.bar_dir:
                    self.count = 1
                return tmp

            self.leg_start_idx = row["leg_start"]
            self.zz_dir = row["zz_direction"]

        if self.leg_start_idx != None and self.zz_dir == self.bar_dir:
            self.count += 1

        if not np.isnan(row["leg_end"]) and self.leg_start_idx == row["leg_end"]:
            tmp = self.count
            self.count = 0
            return tmp

    def run(self, _data):
        return _data.apply(lambda row: self.loop(row), axis=1)
