import backtrader as bt
import pandas as pd

data = pd.read_csv("..\Datasets\AUDCADm_M5_novembro_with_zz.csv")
columns = ['time', 'open', 'high', 'low', 'close', 'zz', 'highs', 'lows']
data = data.loc[:, columns]
# data.set_index('time', inplace=True, drop=True)
data.index = pd.to_datetime(data['time'])
# print(data.head(50))


class PandasData(bt.feed.DataBase):
    '''
    The ``dataname`` parameter inherited from ``feed.DataBase`` is the pandas
    DataFrame
    '''
    lines = ('zz',)
    params = (
        # Possible values for datetime (must always be present)
        #  None : datetime is the "index" in the Pandas Dataframe
        #  -1 : autodetect position or case-wise equal name
        #  >= 0 : numeric index to the colum in the pandas dataframe
        #  string : column name (as index) in the pandas dataframe
        ('datetime', None),

        # Possible values below:
        #  None : column not present
        #  -1 : autodetect position or case-wise equal name
        #  >= 0 : numeric index to the colum in the pandas dataframe
        #  string : column name (as index) in the pandas dataframe
        ('open', -1),
        ('high', -1),
        ('low', -1),
        ('close', -1),
        ('zz', 'zz'),
        ('volume', -1),
        ('openinterest', -1),
    )


data = PandasData(dataname=data)


class strat(bt.Strategy):
    def __init__(self) -> None:
        print(self.data0._name)

    def next(self):
        pass


cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.adddata(data)
cerebro.addstrategy(strat)
cerebro.run()
