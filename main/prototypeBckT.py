import datetime
import csv
import backtrader as bt
import pandas as pd
import numpy as np
from lib.zigzag import zig_zag
from lib.LineBreakoutFailure import LineBreakoutFailure

columns = ['time', 'open', 'high', 'low', 'close']
data = pd.read_csv("../Datasets/AUDCADm_M5_2021_2022_mt5.csv")
# data = data.loc[(data['time'] <= '2022-01-01 00:05:00'), columns]
data = data.loc[(data['time'] >= '2022-01-01 00:00:00')
                & (data['time'] <= '2022-01-10 00:05:00'), columns]
data.reset_index(inplace=True, drop=True)
# data.set_index('datetime', inplace=True, drop=False)

zz, lows, highs, start = zig_zag(data, 12)
data = data.assign(zz=zz, lows=lows, highs=highs, start=start)


lbf = LineBreakoutFailure(data)
lbf.run()
prep = lbf.prepare_backtrader()
# data = data.assign(entries=prep[0])
# nn = data.loc[data['entries'].notnull()]
# print(nn.head(40))
# data.rename(columns={"time": "datetime"}, inplace=True)
# data.index = pd.to_datetime(data['datetime'])


class PandasData(bt.feeds.PandasData):
    '''
    The ``dataname`` parameter inherited from ``feed.DataBase`` is the pandas
    DataFrame
    '''
    lines = ('entries',)
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
        ('entries', -1),
    )

    # datafields = bt.feeds.PandasData.datafields + (['time'])


data = PandasData(dataname=data)


class strat(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.entries = self.datas[0].entries

    def notify_order(self, order):
        # if order.status in [order.Accepted]:
        #     # Buy/Sell order submitted/accepted to/by broker - Nothing to do
        #     return
        # if order.status in [order.Submitted]:
        #     if order.isbuy():
        #         dt, dn = self.datetime.datetime(), order.data._name
        #         print('Buy {} {} {} Price {:.2f} Value {:.2f} Size {} Cash {:.2f}'.format(
        #             order.getstatusname(), dt, dn, order.created.price, order.created.size * order.created.price, order.created.size, self.broker.getcash()))
        #     if order.issell():
        #         dt, dn = self.datetime.datetime(), order.data._name
        #         print('Sell {} {} {} Price {:.2f} Value {:.2f} Size {}'.format(
        #             order.getstatusname(), dt, dn, order.created.price, order.created.size * order.created.price, order.created.size))

        #     # Buy/Sell order submitted/accepted to/by broker - Nothing to do
        #     return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                dt, dn = self.datetime.datetime(), order.data._name
                print('Buy {} {} Price {:.6f} Value {:.6f} Size {}'.format(
                    dt, dn, order.executed.price, order.executed.value, order.executed.size))

            if order.issell():  # Sell
                dt, dn = self.datetime.datetime(), order.data._name
                print('Sell {} {} Price {:.6f} Value {:.6f} Size {}'.format(
                    dt, dn, order.executed.price, order.executed.value, order.executed.size))

        elif order.status in [order.Margin, order.Canceled, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log('Time, {}'.format(self.entries[0]))
        if not np.isnan(self.entries[0]):
            brackets = self.buy_bracket(limitprice=self.dataclose+self.entries+(self.entries*0.05),
                                        price=self.dataclose,
                                        stopprice=self.dataclose-self.entries-0.00005)


# cerebro = bt.Cerebro(stdstats=False)
# cerebro.adddata(data)
# cerebro.addstrategy(strat)
# cerebro.addobserver(bt.observers.BuySell, barplot=True, bardist=0.0)
# cerebro.addsizer(bt.sizers.SizerFix, stake=100000)
# cerebro.broker.setcash(100000000.0)

# print('Starting Portfolio Value: %.6f' % cerebro.broker.getvalue())

# cerebro.run()

# print('Final Portfolio Value: %.6f' % cerebro.broker.getvalue())

# cerebro.plot(volume=False, style='candlestick')

# teste 1:1: 13512
# teste sto +10%: 18532
