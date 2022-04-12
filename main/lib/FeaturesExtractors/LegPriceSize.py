

class LegPriceSize():

    def __init__(self, window) -> None:
        self.window = window
        self.calculated = 0

    def run(self, legs, _data):
        self._data = _data
        sizes = legs.apply(lambda row: self.calc_size(row['leg']), axis=1)
        mean = sizes.rolling(window=self.window).mean()
        # mean, std = self.describe
        return mean

    def calc_size(self, leg):
        mean1 = (self._data.iloc[leg[0]]['low'] +
                 self._data.iloc[leg[0]]['high'])/2
        mean2 = (self._data.iloc[leg[len(leg)-1]]['low'] +
                 self._data.iloc[leg[len(leg)-1]]['high'])/2

        if mean1 <= mean2:
            return abs(self._data.iloc[leg[0]]['low']-self._data.iloc[leg[len(leg)-1]]['high'])
        else:
            return abs(self._data.iloc[leg[0]]['high']-self._data.iloc[leg[len(leg)-1]]['low'])

    def describe(self, sizes):
        mean = sum(sizes)/len(sizes)
        total_size_sum = 0

        for idx in range(len(sizes)):
            total_size_sum += (mean-sizes[idx])**2

        std = sqrt(total_size_sum/len(sizes))

        return mean, std


def ssum(wind):
    print(wind)
