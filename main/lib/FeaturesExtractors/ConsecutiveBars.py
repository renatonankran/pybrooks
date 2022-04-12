from .. import bars


class ConsecutiveBars():

    def __init__(self) -> None:
        self.count = 0
        self.zz_dir = 0
        self.last_bar_dir = 0

    def loop(self, leg, _data):
        self.zz_dir = _data.iloc[leg[0]]["zz_direction"]

        for item in leg:
            bar_dir = bars.bar_direction(_data.iloc[item])
            if self.last_bar_dir == 0 and bar_dir == self.zz_dir:
                self.last_bar_dir = bar_dir
                continue
            if self.last_bar_dir != bar_dir:
                self.last_bar_dir = 0
            if self.last_bar_dir and bar_dir == self.zz_dir:
                self.count += 1

        tmp = self.count+1 if self.count else 0
        self.count = 0
        return tmp

    def run(self, legs, _data):
        return legs.apply(lambda row: self.loop(
            row["leg"], _data), axis=1)
