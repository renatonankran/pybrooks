import numpy as np
import pandas as pd


class TrendDirection():

    def __init__(self, _data) -> None:
        self.compact = _data.loc[_data['zz'].notnull()]
        self.compact.reset_index(inplace=True, drop=False)
        self.compact = self.compact.loc[:, [
            'index', 'zz', 'time', 'highs', 'lows']]
        # print(self.compact.head(30))
        self.c_zz = None
        self.mem = None
        self._direction = 0
        self.plot_dir = 0.0
        self.date_start = self.compact.iloc[0]['time']
        self.count = 0
        self.rev_started = False

    def run(self):

        direction = np.full(self.compact.shape[0], np.nan)
        for idx, item in self.compact.iterrows():
            direction[idx] = self.direction(item['index'])
        self.compact = self.compact.assign(direction=direction)
        tmp = self.prepare_to_plot()
        tmp = pd.DataFrame(tmp.tolist(), columns=[
                           'direction_idx', 'dir_color'])
        self.compact = self.compact.assign(
            direction_idx=tmp['direction_idx'], dir_color=tmp['dir_color'])
        return self.compact

    def prepare_to_plot(self):
        return self.compact.apply(lambda row: self.direction_index2(row), axis=1)

    def direction_index(self, row):
        if self.plot_dir != row['direction']:
            self.plot_dir = row['direction']
            return row['zz'], self.plot_dir
        return np.nan, np.nan

    def direction_index2(self, row):
        if self.plot_dir != row['direction']:
            self.plot_dir = row['direction']
            tmp = self.date_start
            self.date_start = row['time']
            return (tmp, row['time']), self.plot_dir
        return np.nan, np.nan

    def direction(self, zz):
        idx = self.compact[self.compact['index'] == zz].index.item()
        if idx < 6:
            return 0
        if self.c_zz == zz:
            return self._direction

        if self._direction >= 0 and self.compact.iloc[idx]['zz'] == self.compact.iloc[idx]['highs']:
            for idx_zz in range(idx, idx-5, -2):
                if self.compact.iloc[idx_zz]['zz'] < self.compact.iloc[idx_zz-2]['zz']:
                    self.count += 1

            tmp = self.count
            self.count = 0

            if tmp == 3:
                self._direction = -1
                self.c_zz = zz
                return self._direction

        if self._direction <= 0 and self.compact.iloc[idx]['zz'] == self.compact.iloc[idx]['lows']:
            for idx_zz in range(idx, idx-5, -2):
                if self.compact.iloc[idx_zz]['zz'] > self.compact.iloc[idx_zz-2]['zz']:
                    self.count += 1

            tmp = self.count
            self.count = 0

            if tmp == 3:
                self._direction = 1
                self.c_zz = zz
                return self._direction

        return self._direction
