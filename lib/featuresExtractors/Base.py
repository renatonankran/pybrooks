import numpy as np
from lib.zigzag import zz_direction


class Base():
    def __init__(self) -> None:
        self.leg_start_idx = None
        self.leg_idx = -1
        self.direc = []
        self.zz_dir = 0
        self._current = 0

    def loop(self, row):
        # Feature logic goes here:

        if self.leg_end(row):
            self.leg_start_idx = None
        if self.leg_start(row):
            self.leg_start_idx = row.name

    def leg_start(self, row):
        return not np.isnan(row['leg_start'])

    def leg_end(self, row):
        return self.leg_start_idx != None and not np.isnan(row['zz'])

    # def zz_direction(self, row):
    #     zzdirec = zz_direction(row)
    #     if zzdirec != 0:
    #         current = zzdirec
    #     if not np.isnan(row['leg_start']) and not np.isnan(row['zz']):
    #         return zzdirec
    #     else:

    #         return old_dir

    def result(self):
        pass
