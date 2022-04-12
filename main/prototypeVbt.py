import vectorbt as vbt
import pandas as pd
import numpy as np
from lib.zigzag import zig_zag
from lib.ABCFailure import ABCFailure

# data = pd.read_csv("..\Datasets\AUDCADm_M5_novembro_with_zz.csv")
# columns = ['time', 'open', 'high', 'low', 'close', 'zz', 'highs', 'lows']
# data = data.loc[:, columns]

# zz, lows, highs, start = zig_zag(data, 12)
# data = data.assign(zz=zz, lows=lows, highs=highs, start=start)


# abcf = ABCFailure()
# entries, SL, TP = abcf.run(data)

close = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
entries = [True, False, False, False, False, False, False, False, False, False]
sl_stop = [False, False, False, False, False, False, True, False, False, False]

pf = vbt.Portfolio.from_signals(
    close=close, entries=entries, size=0.001, sl_stop=sl_stop)
print(pf.cash())
