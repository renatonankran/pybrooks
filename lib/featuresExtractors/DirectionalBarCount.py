
import numpy as np
from .. import zigzag as zz
import Base
from .. import bars


class directional_bar_count(Base):

    def __init__(self) -> None:
        super().__init__()
        self.counter = 0
        self.zz_direction = None

    def loop(self, row):
        if self.zz_direction != None and bars.bar_direction(row) == self.zz_direction:
            self.counter += 1

        if self.leg_end(row):
            self.leg_start_idx = None
            self.zz_direction = None

            if not np.isnan(row['zz']):
                self.zz_direction = zz.zz_direction(row)

            if self.leg_start(row):
                self.leg_start_idx = row.name

            return self.result()

        if not np.isnan(row['zz']):
            self.zz_direction = zz.zz_direction(row)

        if self.leg_start(row):
            self.leg_start_idx = row.name

        return np.nan

    def result(self):
        tmp = self.counter
        self.counter = 0
        return tmp+1
