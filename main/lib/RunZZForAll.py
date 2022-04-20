from os import listdir
from os.path import isfile, join
from zigzag import zig_zag
import pandas as pd


def RunZZForAll():
    mypath = '../../Datasets/b3'
    mypath_save = '../../Datasets/b3/proceced'

    # name_raw=['B3SA3_M1_2021_2022_mt5.csv',
    #         'B3SA3_M2_2020_2022_mt5.csv',
    #         'B3SA3_M5_2017_2022_mt5.csv',
    #         'BBDC4_M1_2021_2022_mt5.csv',
    #         'BBDC4_M2_2020_2022_mt5.csv',
    #         'BBDC4_M5_2017_2022_mt5.csv',
    #         'ITUB4_M1_2020_2022_mt5.csv',
    #         'ITUB4_M2_2020_2022_mt5.csv',
    #         'ITUB4_M5_2017_2022_mt5.csv',
    #         'B3SA3_M2_2020_2022_mt5.csv',
    #         'B3SA3_M2_2020_2022_mt5.csv',
    #         'B3SA3_M2_2020_2022_mt5.csv',
    #         'B3SA3_M2_2020_2022_mt5.csv',
    #         ]
    for item in listdir(mypath):
        if isfile(join(mypath, item)):
            columns = ['date', 't', 'open', 'high',
                       'low', 'close', 'vol1', 'vol2', 'vol3']
            df = pd.read_csv(join(mypath, item), sep='\t', names=columns,
                             header=0, parse_dates={'time': ['date', 't']})
            columns = ['time', 'open', 'high', 'low', 'close']
            df = df.loc[:, columns]
            word = '_mt5'
            save_name = item.replace(word, '')
            print(save_name)
            for zz_size in [4, 6, 10, 12]:
                zz = zig_zag(df, zz_size)
                df = pd.concat([df, zz], axis=1)
                df.rename(columns={'zz': 'zz'+str(zz_size), 'highs': 'highs'+str(zz_size),
                                   'lows': 'lows'+str(zz_size), 'start': 'start'+str(zz_size)}, inplace=True)
                # print(df.head(40))
                df.to_csv(join(mypath_save, save_name))


RunZZForAll()
