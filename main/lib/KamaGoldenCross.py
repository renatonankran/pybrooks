import talib as ta
import numpy as np


class KamaGoldenCross():
    def __init__(self) -> None:
        pass

    def run(self, _data):
        kama50, kama200 = ta.KAMA(_data['close'], timeperiod=50), ta.KAMA(
            _data['close'], timeperiod=200)
        gcross = np.where(kama50 > kama200, 1, -1)
        return gcross, kama50, kama200
