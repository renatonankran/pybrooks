import numpy as np
import pandas as pd
from pprint import pprint
import plotly.graph_objects as go
from lib.zigzag import zig_zag
from lib.ABCFailure import ABCFailure
from lib.TrendDirection import TrendDirection
from lib.CrossSectionSize import cross_size
from lib.LineBreakoutFailure import LineBreakoutFailure
from lib import LineSide


# data = pd.read_csv("../Datasets/EURUSDm_M30_2021-2022.csv")
data = pd.read_csv("../Datasets/AUDCADm_M5_2021_2022_mt5.csv")
columns = ['time', 'open', 'high', 'low', 'close']
data = data.loc[(data['time'] >= '2022-01-01 00:00:00')
                & (data['time'] <= '2022-01-10 00:05:00'), columns]
data.reset_index(inplace=True, drop=True)

# print(data.tail(40))

zz, lows, highs, start = zig_zag(data, 12)
data = data.assign(zz=zz, lows=lows, highs=highs, start=start)

# print(data.loc[data['zz'].notnull()].head(30))

lbf = LineBreakoutFailure(data)
lbf.run()
prep = lbf.prepare_backtrader()
# x=data['time'],
fig = go.Figure(data=[go.Candlestick(open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'])])

fig.add_trace(go.Scatter(
    x=data.loc[(data['zz'].notnull())].index,
    y=data.loc[(data['zz'].notnull())]['zz']
))
fig.add_trace(go.Scatter(
    x=data.loc[(data['start'].notnull())].index,
    y=data.loc[(data['start'].notnull())]['start'],
    mode="markers",
    marker=dict(color="black")
))


# fig.add_trace(go.Scatter(
#     x=[x for x in range(27, 67)],
#     y=line,
# ))

# fig.add_trace(go.Scatter(
#     x=data.loc[(data['SL'].notnull())]['time'],
#     y=data.loc[(data['SL'].notnull())]['SL'],
#     mode="markers",
#     marker=dict(color="orange")
# ))
# fig.add_trace(go.Scatter(
#     x=data.loc[(data['TP'].notnull())]['time'],
#     y=data.loc[(data['TP'].notnull())]['TP'],
#     mode="markers",
#     marker=dict(color="blue")
# ))

# for idx, item in td_df.loc[(td_df['dir_color'].notnull())].iterrows():
#     if item['dir_color'] == 1:
#         fig.add_vrect(
#             x0=item['direction_idx'][0], x1=item['direction_idx'][1],
#             fillcolor="LightSalmon", opacity=0.4,
#             layer="below", line_width=0,
#         )
#     if item['dir_color'] == -1:
#         fig.add_vrect(
#             x0=item['direction_idx'][0], x1=item['direction_idx'][1],
#             fillcolor="LightGreen", opacity=0.4,
#             layer="below", line_width=0,
#         )

# fig.update_xaxes(
#     rangebreaks=[
#         dict(bounds=["sat", "mon"]),  # hide weekends
#     ]
# )
# fig.update_layout(xaxis_rangeslider_visible=False)

# fig.show()
