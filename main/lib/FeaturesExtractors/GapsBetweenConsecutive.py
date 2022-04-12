from matplotlib.pyplot import bar_label
from .. import bars


class GapsBetweenConsecutive():

    def __init__(self) -> None:
        self.count = 0
        self.zz_dir = 0
        self.gap = False

    def loop(self, leg, _data):
        self.zz_dir = _data.iloc[leg[0]]["zz_direction"]

        for item in range(len(leg)-2):
            for second_item in range(item+2, len(leg)):
                self.gap = bars.gap(
                    _data.iloc[leg[item]], _data.iloc[leg[second_item]])
                print("self.gap: ", self.gap)
                if second_item == item+2:
                    if self.gap:
                        self.count += 1
                    else:
                        break
                else:
                    if self.count > 0:
                        if not self.gap:
                            self.count -= 1

        tmp = self.count
        self.count = 0
        return tmp

    def run(self, legs, _data):
        return legs.apply(lambda row: self.loop(
            row["leg"], _data), axis=1)
