import numpy as np
import pandas as pd
import plotly.graph_objects as go
from lib.zigzag import zig_zag
from lib.FindLegStart import FindLegStart
from lib.FindLegEnd import FindLegEnd
from lib.ABCFailure import ABCFailure
from lib.TrendDirection import TrendDirection
from lib.KamaGoldenCross import KamaGoldenCross
from lib.bars import gap
from lib.AbstractLegs import AbstractLegs
from lib.FeaturesExtractors.BarCountage import BarCountage
from lib.FeaturesExtractors.DirectionalBarCount import DirectionalBarCount
from lib.FeaturesExtractors.LegReversalAttempts import LegReversalAttempts
from lib.FeaturesExtractors.MicroTradingRange import MicroTradingRange
from lib.FeaturesExtractors.ConsecutiveBars import ConsecutiveBars
from lib.FeaturesExtractors.GapsBetweenConsecutive import GapsBetweenConsecutive
from lib.FeaturesExtractors.LegPriceSize import LegPriceSize


# columns = ['date', 't', 'open', 'high', 'low', 'close', 'vol1', 'vol2', 'vol3']
# data = pd.read_csv("..\Datasets\AUDCADm_M5_novembro_with_zz.csv")
# columns = ['time', 'open', 'high', 'low', 'close', 'zz', 'highs', 'lows']
# data = data.loc[:, columns]

data = pd.read_csv("../Datasets/EURUSDm_M30_2021-2022.csv")
datam5 = pd.read_csv("../Datasets/EURUSDm_M5_2021_2022.csv")
columns = ['time', 'open', 'high', 'low', 'close']
# data = data.loc[(data['time'] >= '2021-12-01 00:00:00')
#                 & (data['time'] <= '2021-12-31 00:00:00'), columns]
# data.reset_index(inplace=True, drop=True)
# parsed_df.reset_index(inplace=True, drop=True)


# fls = FindLegStart()
# fls_df = fls.run(parsed_df)
# parsed_df = pd.concat([parsed_df, fls_df], axis=1)

# fle = FindLegEnd()
# fle_df = fle.run(parsed_df)
# parsed_df = parsed_df.assign(leg_end=fle_df)

# lra = LegReversalAttempts()
# lra_df = lra.run(parsed_df)

# al = AbstractLegs()
# al_df = al.run(parsed_df)
# al_df = pd.DataFrame(al_df, columns=["leg"]).reset_index()

# mtr = MicroTradingRange()
# mtr.run(al_df, parsed_df)

# gbc = GapsBetweenConsecutive()
# cgb_df = gbc.run(al_df, parsed_df)

# lps = LegPriceSize(window=5)
# lps_df = lps.run(al_df, parsed_df)

zz, lows, highs, start = zig_zag(data, 12)
data = data.assign(zz=zz, lows=lows, highs=highs, start=start)

# print(data.head(30))

# kgc = KamaGoldenCross()
# gcross, kama50, kama200 = kgc.run(data)
# data = data.assign(direction=gcross, kama50=kama50, kama200=kama200)

td = TrendDirection(data)
td_df = td.run()
# td_df = pd.DataFrame(td_df.tolist(), columns=['direction_idx', 'dir_color'])
print(td_df.tail(40))

# abcf = ABCFailure()
# entries, SL, TP = abcf.run(data)
# data = data.assign(entries=entries, SL=SL, TP=TP)

fig = go.Figure(data=[go.Candlestick(x=datam5['time'], open=datam5['open'],
                high=datam5['high'],
                low=datam5['low'],
                close=datam5['close'])])

fig.add_trace(go.Scatter(
    x=data.loc[(data['zz'].notnull())]['time'],
    y=data.loc[(data['zz'].notnull())]['zz']
))

# fig.add_trace(go.Scatter(
#     x=data['time'],
#     y=data['kama50']
# ))
# fig.add_trace(go.Scatter(
#     x=data['time'],
#     y=data['kama200']
# ))


# fig.add_trace(go.Scatter(
#     x=data.loc[(data['entries'].notnull())]['time'],
#     y=data.loc[(data['entries'].notnull())]['entries'],
#     mode="markers",
#     marker=dict(color="black")
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

for idx, item in td_df.loc[(td_df['dir_color'].notnull())].iterrows():
    if item['dir_color'] == 1:
        fig.add_vrect(
            x0=item['direction_idx'][0], x1=item['direction_idx'][1],
            fillcolor="LightSalmon", opacity=0.4,
            layer="below", line_width=0,
        )
    if item['dir_color'] == -1:
        fig.add_vrect(
            x0=item['direction_idx'][0], x1=item['direction_idx'][1],
            fillcolor="LightGreen", opacity=0.4,
            layer="below", line_width=0,
        )

fig.update_xaxes(
    rangebreaks=[
        dict(bounds=["sat", "mon"]),  # hide weekends
    ]
)
fig.update_layout(xaxis_rangeslider_visible=False)

fig.show()
