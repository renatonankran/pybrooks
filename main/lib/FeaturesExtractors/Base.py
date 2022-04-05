import numpy as np


class Base():
    def __init__(self) -> None:
        self.leg_start_idx = None
        self.zz_dir = 0

    def loop(self, row):
        # Feature logic goes here:

        if self.leg_ended(row):
            pass
        if self.leg_started(row):
            pass

    def leg_started(self, row):
        if not np.isnan(row['leg_start']) or self.leg_start_idx != None:
            self.leg_start_idx = row["leg_start"]
            self.zz_dir = row["zz_direction"]
            return True
        return False

    def leg_ended(self, row):
        if not np.isnan(row["leg_end"]):
            self.leg_start_idx = None
            self.zz_dir = 0
            return True
        return False

    def result(self):
        pass
#  and row["leg_end"] == self.leg_start_idx