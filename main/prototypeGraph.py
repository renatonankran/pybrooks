import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from math import sqrt
data = pd.read_csv("..\Datasets\WDO@_M5-with-zz.csv")
# data['time'] = pd.to_datetime(data['time'], unit='ms')
columns = ['time', 'open', 'high', 'low', 'close', 'zz']
data = data.loc[(data['time'] >= '2021-03-10 8:00:00') &
                (data['time'] <= '2021-03-15 19:00:00'), columns]
data.reset_index(inplace=True, drop=True)

total_sum = 0
for idx in range(data.shape[0]):
    total_sum += data.iloc[idx]['high']-data.iloc[idx]['low']
mean = total_sum/data.shape[0]
# print("mean: ", mean)

total_sum = 0
for idx in range(data.shape[0]):
    total_sum += (mean-(data.iloc[idx]['high']-data.iloc[idx]['low']))**2

bar_std = sqrt(total_sum/data.shape[0])

leg_sizes = []
high_idx = low_idx = None
for idx in range(data.shape[0]):
    if data.iloc[idx]['zz'] != None:
        if data.iloc[idx]['zz'] == data.iloc[idx]['high']:
            high_idx = idx
        if data.iloc[idx]['zz'] == data.iloc[idx]['low']:
            low_idx = idx
        if high_idx != None and low_idx != None:
            leg_sizes.append(dict(size=abs(data.iloc[high_idx]['zz']-data.iloc[low_idx]['zz']),
                                  idx=[low_idx, high_idx]))
            if low_idx == idx:
                high_idx = None
            else:
                low_idx = None

total_size_sum = 0
for idx in range(len(leg_sizes)):
    total_size_sum += leg_sizes[idx]['size']

leg_mean = total_size_sum/len(leg_sizes)
# print(leg_mean)

total_size_sum = 0
for idx in range(len(leg_sizes)):
    total_size_sum += (leg_mean-leg_sizes[idx]['size'])**2

leg_std = sqrt(total_size_sum/len(leg_sizes))
# print(leg_std)

bigger_legs = list()
for idx in range(len(leg_sizes)):
    if leg_sizes[idx]['size'] > leg_mean:
        bigger_legs.append(leg_sizes[idx]['idx'])

fig = make_subplots(rows=3, cols=1)

fig.add_trace(go.Candlestick(x=data['time'],
                             open=data['open'],
                             high=data['high'],
                             low=data['low'],
                             close=data['close']),
              row=1, col=1)

fig.add_trace(go.Scatter(
    x=data.loc[(data['zz'].notnull())]['time'],
    y=data.loc[(data['zz'].notnull())]['zz']
))

bigger_than = data.loc[(abs(data['open']-data['close']) >= mean)]
fig.add_trace(go.Candlestick(x=bigger_than['time'],
                             open=bigger_than['open'],
                             high=bigger_than['high'],
                             low=bigger_than['low'],
                             close=bigger_than['close']),
              row=2, col=1)


fig.add_trace(go.Candlestick(x=data['time'],
                             open=data['open'],
                             high=data['high'],
                             low=data['low'],
                             close=data['close']),
              row=3, col=1)


for idx in range(len(bigger_legs)):
    fig.add_shape(type="line",
                  x0=data.loc[bigger_legs[idx][0]]['time'],
                  y0=data.loc[bigger_legs[idx][0]]['zz'],
                  x1=data.loc[bigger_legs[idx][1]]['time'],
                  y1=data.loc[bigger_legs[idx][1]]['zz'],
                  line=dict(color="black", width=4), row=3, col=1
                  )

fig.update_xaxes(
    rangebreaks=[
        dict(bounds=["sat", "mon"]),  # hide weekends
        dict(bounds=[19, 9], pattern="hour"),  # hide hours outside of 9am-6pm
    ]
)
fig.update_layout(xaxis_rangeslider_visible=False,
                  xaxis2_rangeslider_visible=False, xaxis3_rangeslider_visible=False)
fig.show()

# print(data.tail())
