from os import listdir
from os.path import isfile, join
from pprint import pprint
import backtrader as bt
import pandas as pd
import numpy as np
from lib.LineBreakoutFailure import LineBreakoutFailure
from lib.zigzag import zig_zag


columns = ['time', 'open', 'high', 'low', 'close']
data = pd.read_csv("../Datasets/AUDCADm_M5_2021_2022.csv")
# data = data.loc[(data['time'] <= '2022-01-01 00:05:00'), columns]
data = data.loc[(data['time'] >= '2022-01-01 00:00:00')
                & (data['time'] <= '2022-01-10 00:05:00'), columns]
data.reset_index(inplace=True, drop=True)
# data.set_index('datetime', inplace=True, drop=False)

df = zig_zag(data, 6)
data = pd.concat([data, df], axis=1)

lbf = LineBreakoutFailure(data)
lbf.run()
prep = lbf.prepare_backtrader()
data = data.assign(entries=prep[0])
nn = data.loc[data['entries'].notnull()]
print(nn.head(40))
data.rename(columns={"time": "datetime"}, inplace=True)
data.index = pd.to_datetime(data['datetime'])

mypath = "../Datasets/b3/proceced"


def run():
    for item in listdir(mypath):
        if isfile(join(mypath, item)):
            if item == 'B3SA3_M5_2017_2022.csv':
                data = pd.read_csv(join(mypath, item))
                for zz_size in [4, 6, 10, 12]:
                    columns = ['time', 'open', 'high', 'low', 'close', 'zz' +
                               str(zz_size), 'highs'+str(zz_size), 'lows'+str(zz_size), 'start'+str(zz_size)]
                    parsed = data.loc[:, columns]
                    rename_cols = {'zz'+str(zz_size): 'zz',
                                   'highs'+str(zz_size): 'highs',
                                   'lows'+str(zz_size): 'lows',
                                   'start'+str(zz_size): 'start'}
                    parsed.rename(columns=rename_cols, inplace=True)

                    lbf = LineBreakoutFailure(parsed)
                    lbf.run()
                    prep = lbf.prepare_backtrader()
                    for idx in range(2):
                        parsed = parsed.assign(entries=prep[idx])
                        parsed.rename(
                            columns={"time": "datetime"}, inplace=True)
                        parsed.index = pd.to_datetime(parsed['datetime'])
                        nn = parsed.loc[parsed['entries'].notnull()]
                        print(nn.head(20))


# run()


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

    # def notify_order(self, order):

        #     # if order.status in [order.Accepted]:
        #     #     # Buy/Sell order submitted/accepted to/by broker - Nothing to do
        #     #     return
        #     # if order.status in [order.Submitted]:
        #     #     if order.isbuy():
        #     #         dt, dn = self.datetime.datetime(), order.data._name
        #     #         print('Buy {} {} {} Price {:.2f} Value {:.2f} Size {} Cash {:.2f}'.format(
        #     #             order.getstatusname(), dt, dn, order.created.price, order.created.size * order.created.price, order.created.size, self.broker.getcash()))
        #     #     if order.issell():
        #     #         dt, dn = self.datetime.datetime(), order.data._name
        #     #         print('Sell {} {} {} Price {:.2f} Value {:.2f} Size {}'.format(
        #     #             order.getstatusname(), dt, dn, order.created.price, order.created.size * order.created.price, order.created.size))

        #     #     # Buy/Sell order submitted/accepted to/by broker - Nothing to do
        #     #     return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        # if order.status in [order.Completed]:
        #     if order.isbuy():
        #         dt, dn = self.datetime.datetime(), order.data._name
        #         print('Buy {} {} Price {:.6f} Value {:.6f} Size {}'.format(
        #             dt, dn, order.executed.price, order.executed.value, order.executed.size))

        #     if order.issell():  # Sell
        #         dt, dn = self.datetime.datetime(), order.data._name
        #         print('Sell {} {} Price {:.6f} Value {:.6f} Size {}'.format(
        #             dt, dn, order.executed.price, order.executed.value, order.executed.size))

        # elif order.status in [order.Margin, order.Canceled, order.Rejected]:
        #     self.log('Order Canceled/Margin/Rejected')

    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log('Time, {}'.format(self.entries[0]))
        if not np.isnan(self.entries[0]):
            brackets = self.buy_bracket(limitprice=self.dataclose+self.entries,
                                        price=self.dataclose,
                                        stopprice=(self.dataclose-self.entries))


cerebro = bt.Cerebro(stdstats=False)
cerebro.adddata(data)
cerebro.addstrategy(strat)
cerebro.addobserver(bt.observers.BuySell, barplot=True, bardist=0.0)
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='ta')
cerebro.addsizer(bt.sizers.SizerFix, stake=1)
cerebro.broker.setcash(100000000.0)

print('Starting Portfolio Value: %.5f' % cerebro.broker.getvalue())

thestrats = cerebro.run()
thestrat = thestrats[0]
ta = thestrat.analyzers.ta.get_analysis()
pprint('total trades:         %.1f' % ta['total']['total'])
pprint('pnl net total:        %.5f' % ta['pnl']['net']['total'])
pprint('pnl net average:      %.5f' % ta['pnl']['net']['average'])
pprint('win trades:           %.5f' % ta['won']['total'])
pprint('win total:            %.5f' % ta['won']['pnl']['total'])
pprint('win average:          %.5f' % ta['won']['pnl']['average'])
pprint('loss trades:          %.5f' % ta['lost']['total'])
pprint('loss total:           %.5f' % ta['lost']['pnl']['total'])
pprint('loss average:         %.5f' % ta['lost']['pnl']['average'])

# cerebro.plot(volume=False, style='candlestick')

# teste 1:1: 13512
# teste sto +10%: 18532
