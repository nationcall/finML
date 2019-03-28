# define functions to generate bars
import numpy as np


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
    dol_cum = np.cumsum(raw_data['size']*raw_data['price'])//num_dollar
    diff = np.diff(dol_cum, 1)
    diff = np.insert(diff,0,0)
    bool_diff = (diff == 1)
    dbs = raw_data.loc[bool_diff]
    print(dbs.head())
    return dbs

# 2.1(b)
def count_bars_per_week(bars):
    wk_num = 

import pandas as pd

raw_file = "IVE_tickbidask.txt"
cols = ['date','time','price','bid','ask','size']
raw_data = (pd.read_csv(raw_file,nrows=5000,header=None)
            .rename(columns=dict(zip(range(len(cols)),cols))))
#raw_data.head()
tbs, vbs, dbs = tick_bars(raw_data), volume_bars(raw_data), dollar_bars(raw_data)
