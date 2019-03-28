# define functions to generate bars
import numpy as np
import matplotlib.pyplot as plt


def tick_bars(raw_data, num_ticks=1000):
    '''
    :param raw_data: time bars
            num_ticks: number of ticks to sample
    :return: tick bars
    '''
    #inds = range(0, 10000, 1000)
    inds = range(0, raw_data.shape[0], num_ticks)
    tbs = raw_data.loc[inds]
    return tbs


def volume_bars(raw_data, num_vol=1000):
    vols = np.cumsum(raw_data['size'])//num_vol
    diff = np.diff(vols, 1)
    diff = np.insert(diff,0,0)
    #print(diff.sum())
    bool_diff = (diff == 1)
    vbs = raw_data.loc[bool_diff]
    print(vbs.head())
    return vbs


def dollar_bars(raw_data, num_dollar=1e6):
    dol_cum = np.cumsum(raw_data['dollar_vol'])//num_dollar
    diff = np.diff(dol_cum, 1)
    diff = np.insert(diff, 0, 0)
    bool_diff = (diff == 1)
    dbs = raw_data.loc[bool_diff]
    print(dbs.head())
    return dbs


def count_bars_per_week(bars): #count number of bars by week
    count_week = bars.assign(count=1)
    wk_num = count_week['count'].resample('W').sum()
    return wk_num


import pandas as pd

raw_file = "IVE_tickbidask.txt"
cols = ['date','time','price','bid','ask','size']
raw_data = (pd.read_csv(raw_file, nrows=50000, header=None)
            .rename(columns=dict(zip(range(len(cols)), cols)))
            .assign(dates=lambda df:pd.to_datetime(df['date']+df['time'], format='%m/%d/%Y%H:%M:%S'))
            .assign(dollar_vol=lambda df:df['size']*df['price'])
            .drop(['date', 'time'], axis=1)
            .set_index('dates')
            .drop_duplicates())
#print(raw_data.head())
tbs, vbs, dbs = tick_bars(raw_data), volume_bars(raw_data), dollar_bars(raw_data)
#count_bars_per_week(raw_data)

# 2.1(b)
tbs_wk, vbs_wk, dbs_wk = count_bars_per_week(tbs), count_bars_per_week(vbs), count_bars_per_week(dbs)
plt.plot(tbs_wk)
