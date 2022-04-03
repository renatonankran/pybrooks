import numpy as np


class base():
    def __init__(self) -> None:
        self.leg_start_idx = None

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

    def result(self):
        pass
