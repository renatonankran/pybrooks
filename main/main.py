import numpy as np
import pandas as pd
from lib.FindLegStart import FindLegStart
from lib.FindLegEnd import FindLegEnd
from lib.FeaturesExtractors.BarCountage import BarCountage
from lib.FeaturesExtractors.DirectionalBarCount import DirectionalBarCount


data = pd.read_csv("..\Datasets\WDO@_M5-with-zz.csv")
columns = ['time', 'open', 'high', 'low', 'close', 'zz', 'highs', 'lows']
parsed_df = data.loc[(data['time'] >= '2021-03-22 09:00:00')
                     & (data['time'] <= '2021-03-22 19:00:00')]
parsed_df = parsed_df.loc[:, columns]
parsed_df.reset_index(inplace=True, drop=True)

fls = FindLegStart()
fls_df = fls.run(parsed_df)
parsed_df = pd.concat([parsed_df, fls_df], axis=1)

fle = FindLegEnd()
fle_df = fle.run(parsed_df)
parsed_df = parsed_df.assign(leg_end=fle_df)

dbc = DirectionalBarCount()
dbc_df = dbc.run(parsed_df)

print(dbc_df.head(50))
