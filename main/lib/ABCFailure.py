import numpy as np


class ABCFailureNoSide():

    def __init__(self) -> None:
        pass

    def run(self, _data):
        extries = self.separate_abc_extremes(_data)
        sl, tp = self.SLnTP(_data)
        return extries, sl, tp

    def separate_abc_extremes(self, _data):
        failure = np.full(_data.shape[0], np.nan)
        zz = _data.loc[(_data['zz'].notnull())]
        zz.reset_index(inplace=True, drop=False)
        for idx in range(len(zz)-3):
            if zz.iloc[idx]['zz'] > zz.iloc[idx+1]['zz'] and zz.iloc[idx+3]['zz'] > zz.iloc[idx+1]['zz'] and zz.iloc[idx]['zz'] > zz.iloc[idx+2]['zz']:
                failure[zz.iloc[idx+2]['index']] = zz.iloc[idx+2]['zz']
            if zz.iloc[idx]['zz'] < zz.iloc[idx+1]['zz'] and zz.iloc[idx+3]['zz'] < zz.iloc[idx+1]['zz'] and zz.iloc[idx]['zz'] < zz.iloc[idx+2]['zz']:
                failure[zz.iloc[idx+2]['index']] = zz.iloc[idx+2]['zz']
        return failure

    def SLnTP(self, _data):
        sl = np.full(_data.shape[0], np.nan)
        tp = np.full(_data.shape[0], np.nan)
        zz = _data.loc[(_data['zz'].notnull())]
        zz.reset_index(inplace=True, drop=False)
        for idx in range(len(zz)-3):
            if zz.iloc[idx]['zz'] > zz.iloc[idx+1]['zz'] and zz.iloc[idx+3]['zz'] > zz.iloc[idx+1]['zz'] and zz.iloc[idx]['zz'] > zz.iloc[idx+2]['zz']:
                size1 = zz.iloc[idx+2]['zz']-zz.iloc[idx+1]['zz']
                size2 = zz.iloc[idx]['zz']-zz.iloc[idx+2]['zz']
                if size1 >= size2:
                    sl[zz.iloc[idx+2]['index']] = zz.iloc[idx+2]['zz']+size1
                    tp[zz.iloc[idx+2]['index']] = zz.iloc[idx+2]['zz']-size1
                else:
                    sl[zz.iloc[idx+2]['index']] = zz.iloc[idx+2]['zz']+size2
                    tp[zz.iloc[idx+2]['index']] = zz.iloc[idx+2]['zz']-size2
            if zz.iloc[idx]['zz'] < zz.iloc[idx+1]['zz'] and zz.iloc[idx+3]['zz'] < zz.iloc[idx+1]['zz'] and zz.iloc[idx]['zz'] < zz.iloc[idx+2]['zz']:
                size1 = zz.iloc[idx+1]['zz']-zz.iloc[idx+2]['zz']
                size2 = zz.iloc[idx+2]['zz']-zz.iloc[idx]['zz']
                if size1 >= size2:
                    sl[zz.iloc[idx+2]['index']] = zz.iloc[idx+2]['zz']-size1
                    tp[zz.iloc[idx+2]['index']] = zz.iloc[idx+2]['zz']+size1
                else:
                    sl[zz.iloc[idx+2]['index']] = zz.iloc[idx+2]['zz']-size2
                    tp[zz.iloc[idx+2]['index']] = zz.iloc[idx+2]['zz']+size2
        return sl, tp


class ABCFailure():

    def __init__(self) -> None:
        pass

    def run(self, _data):
        return self.separate_abc_extremes(_data)

    def separate_abc_extremes(self, _data):
        zz = _data.loc[(_data['zz'].notnull())]
        entry = np.full(_data.shape[0], np.nan)
        sl = np.full(_data.shape[0], np.nan)
        tp = np.full(_data.shape[0], np.nan)
        zz.reset_index(inplace=True, drop=False)
        # print(zz.head(40))
        for idx in range(len(zz)-3):
            if zz.iloc[idx+3]['direction'] < 0:
                # print(zz.iloc[idx+3]['direction'])
                if zz.iloc[idx]['zz'] > zz.iloc[idx+1]['zz'] and zz.iloc[idx+3]['zz'] > zz.iloc[idx+1]['zz']:
                    entry[zz.iloc[idx+2]['index']] = zz.iloc[idx+2]['zz']
                    size1 = zz.iloc[idx+2]['zz']-zz.iloc[idx+1]['zz']
                    size2 = zz.iloc[idx]['zz']-zz.iloc[idx+2]['zz']
                    if size1 >= size2:
                        sl[zz.iloc[idx+2]['index']
                           ] = zz.iloc[idx+2]['zz']+size1+0.00030
                        tp[zz.iloc[idx+2]['index']] = zz.iloc[idx+2]['zz']-size1
                    else:
                        sl[zz.iloc[idx+2]['index']
                           ] = zz.iloc[idx+2]['zz']+size2+0.00030
                        tp[zz.iloc[idx+2]['index']] = zz.iloc[idx+2]['zz']-size2
            if zz.iloc[idx+3]['direction'] > 0:
                # print(zz.iloc[idx+3]['direction'])
                if zz.iloc[idx]['zz'] < zz.iloc[idx+1]['zz'] and zz.iloc[idx+3]['zz'] < zz.iloc[idx+1]['zz']:
                    entry[zz.iloc[idx+2]['index']] = zz.iloc[idx+2]['zz']
                    size1 = zz.iloc[idx+1]['zz']-zz.iloc[idx+2]['zz']
                    size2 = zz.iloc[idx+2]['zz']-zz.iloc[idx]['zz']
                    if size1 >= size2:
                        sl[zz.iloc[idx+2]['index']
                           ] = zz.iloc[idx+2]['zz']-size1-0.00030
                        tp[zz.iloc[idx+2]['index']] = zz.iloc[idx+2]['zz']+size1
                    else:
                        sl[zz.iloc[idx+2]['index']
                           ] = zz.iloc[idx+2]['zz']-size2-0.00030
                        tp[zz.iloc[idx+2]['index']] = zz.iloc[idx+2]['zz']+size2
        return entry, sl, tp
