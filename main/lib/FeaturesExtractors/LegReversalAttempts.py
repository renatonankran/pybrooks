import numpy as np
from .. import bars


class LegReversalAttempts():
    def __init__(self) -> None:
        super().__init__()
        self.count = 0
        self.reversed = False
        self.reversed_count = 0
        self.doji = False
        self.leg_start_idx = None
        self.zz_dir = None

    def loop(self, row):
        self.bar_dir = bars.bar_direction(row)
        self.doji = bars.doji(row)
        if not np.isnan(row["leg_start"]):
            if not np.isnan(row["leg_end"]) and self.leg_start_idx == row["leg_end"]:
                if self.count > 0 and self.bar_dir != 0 and self.bar_dir != self.zz_dir:
                    self.count = 0
                    self.reversed_count += 1
                    if not self.doji:
                        self.count += 1
                    tmp = self.reversed_count
                    self.reversed_count = 0
                    self.leg_start_idx = row["leg_start"]
                    self.zz_dir = row["zz_direction"]
                    # print(row.name)
                    return tmp
            self.leg_start_idx = row["leg_start"]
            self.zz_dir = row["zz_direction"]

        if self.leg_start_idx != None:
            if not self.doji and self.bar_dir == self.zz_dir:
                self.count += 1
            if self.count > 0 and self.bar_dir != 0 and self.bar_dir != self.zz_dir:
                self.count = 0
                self.reversed_count += 1
        # if row.name in [4]:
        #     print(self.count, self.reversed_count)
        if not np.isnan(row["leg_end"]):
            tmp = self.reversed_count
            self.reversed_count = 0
            return tmp

    def run(self, _data):
        return _data.apply(lambda row: self.loop(row), axis=1)
