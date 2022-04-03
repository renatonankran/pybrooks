import numpy as np


def zig_zag(data, depth):
    backstep = depth
    highs = np.full(data.shape[0], np.nan)
    lows = np.full(data.shape[0], np.nan)
    last_high = data.iloc[0]['high']
    last_low = data.iloc[0]['low']

    for idx, _ in data.iterrows():
        if idx < depth:
            continue
        max = np.amax(data[idx-depth:idx]['high'])
        min = np.amin(data[idx-depth:idx]['low'])
        if max == data.iloc[idx-1]['high'] and last_high != max:
            highs[idx-1] = max
            last_high = max
        if min == data.iloc[idx-1]['low'] and min != last_low:
            lows[idx-1] = min
            last_low = min

        for b in range(2, backstep+1):
            if not np.isnan(lows[idx-1]) and not np.isnan(lows[idx-b]) and lows[idx-b] > lows[idx-1]:
                lows[idx-b] = np.nan
            if not np.isnan(highs[idx-1]) and not np.isnan(highs[idx-b]) and highs[idx-b] < highs[idx-1]:
                highs[idx-b] = np.nan

    zz = np.full(data.shape[0], np.nan)

    for idx in range(0, data.shape[0]):

        if not np.isnan(highs[idx]):
            zz[idx] = highs[idx]

            for last in reversed(range(idx)):
                if not np.isnan(zz[last]):
                    if zz[last] != highs[last]:
                        break
                    if zz[last] == highs[last]:
                        if zz[last] >= zz[idx]:
                            zz[idx] = np.nan
                            break
                        else:
                            zz[last] = np.nan
                            break

        if not np.isnan(lows[idx]):
            zz[idx] = lows[idx]

            for last in reversed(range(idx)):
                if not np.isnan(zz[last]):
                    if zz[last] != lows[last]:
                        break
                    if zz[last] == lows[last]:
                        if zz[last] <= zz[idx]:
                            zz[idx] = np.nan
                            break
                        else:
                            zz[last] = np.nan
                            break

    return zz, lows, highs


def zz_direction(row):
    if row['zz'] != np.nan:
        if row["zz"] == row["highs"]:
            return -1
        else:
            return 1
    return 0
