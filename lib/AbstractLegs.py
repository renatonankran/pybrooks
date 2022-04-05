import pandas as pd
import numpy as np
import bars
from zigzag import zz_direction


class AbstractLegs():

    def __init__(self) -> None:
        self.current = []
        self.next = []
        self.leg_start = None
        self.zz = 0
        self.curr_leg_idx = 0

    def loop(self, row):
        if not np.isnan(row['leg_start']):
            self.leg_start = row['leg_start']

        if not np.isnan(row['zz']):
            self.zz_dir = zz_direction(row)

        bar_dir = bars.bar_direction(row)

        if self.leg_start:
            if len(self.current) > 0:
                self.current.append(row.name)

                if not np.isnan(row['zz']):
                    self.leg_start = None

                    if not np.isnan(row['leg_start']):
                        self.next.append(row.name)
                        self.leg_start = row['leg_start']

                    tmp = self.current
                    self.current = []
                    return tmp
            elif len(self.next) > 0:
                self.next.append(row.name)

                if not np.isnan(row['zz']):
                    self.leg_start = None

                    if not np.isnan(row['leg_start']):
                        self.current.append(row.name)
                        self.leg_start = row['leg_start']

                    tmp = self.next
                    self.next = []
                    return tmp
            else:
                self.current.append(row.name)

                if not np.isnan(row['zz']) and self.zz_dir != bar_dir and not np.isnan(row['leg_start']):
                    tmp = self.current
                    self.current = []
                    return tmp

    def run(self, _data):
        legb = _data.apply(lambda row: self.loop(row), axis=1)
        return legb.loc[~pd.isnull(legb)]
