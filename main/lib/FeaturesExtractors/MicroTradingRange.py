from .. import bars


class MicroTradingRange():

    def __init__(self) -> None:
        self.overlaping_count = 0
        self.overlap_flag = False
        self.last_overlaping_bar = 0

    def run(self, legs, _data):
        # legs.apply(lambda row: self.loop(
        #     row["leg"], _data), axis=1)
        self.loop(legs.iloc[10]["leg"], _data)

    def loop(self, leg, _data):
        self.leg = leg
        idx = 0
        while idx < len(leg)-1:
            bar_before = leg[idx]
            doji = bars.doji(_data.iloc[bar_before])
            if not doji:
                for overlap_bar in range(2, len(leg)-idx):
                    self.overlap_flag = bars.inside_bar(_data.iloc[bar_before], _data.iloc[bar_before+overlap_bar]) or \
                        bars.inside_bar(_data.iloc[bar_before], _data.iloc[bar_before+overlap_bar], inside_body=True) or \
                        bars.between(_data.iloc[bar_before]['close'], _data.iloc[bar_before+overlap_bar]) or \
                        bars.between(
                            _data.iloc[bar_before]['open'], _data.iloc[bar_before+overlap_bar])

                    if bar_before+overlap_bar == bar_before+2:
                        if not self.overlap_flag:
                            break
                    if self.overlap_flag:
                        self.overlaping_count += 1
                        self.last_overlaping_bar = bar_before+overlap_bar
            else:
                for overlap_bar in range(2, len(leg)-idx):
                    self.overlap_flag = bars.inside_bar(_data.iloc[bar_before], _data.iloc[bar_before+overlap_bar]) or \
                        bars.inside_bar(_data.iloc[bar_before], _data.iloc[bar_before+overlap_bar], inside_body=True) or \
                        bars.between(_data.iloc[bar_before]['high'], _data.iloc[bar_before+overlap_bar]) or \
                        bars.between(_data.iloc[bar_before]
                                     ['low'], _data.iloc[bar_before+overlap_bar])
                    print("self.overlap_flag: ", self.overlap_flag,
                          bar_before+overlap_bar)
                    if bar_before+overlap_bar == bar_before+2:
                        if not self.overlap_flag:
                            break
                    if self.overlap_flag:
                        self.overlaping_count += 1
                        self.last_overlaping_bar = bar_before+overlap_bar

            if self.last_overlaping_bar > bar_before:
                idx = leg.index(self.last_overlaping_bar)
                print('idx: ', self.last_overlaping_bar)
            else:
                idx = leg.index(bar_before+1)
