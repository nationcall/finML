# define functions to generate bars
import numpy as np
import matplotlib.pyplot as plt


def sample_data(raw_data, ratio=0.1):
    # stratified sampling based on date from original raw data
    shuffled_indices = np.random.permutation(raw_data.shape[0])
    sampled_size = int(raw_data.shape[0]*ratio)
    sampled_indices = shuffled_indices[:sampled_size]
    return raw_data.iloc[sampled_indices]


def tick_bars(raw_data, num_ticks=1000):
    '''
    :param raw_data: time bars
            num_ticks: number of ticks to sample
    :return: tick bars
    '''
    #inds = range(0, 10000, 1000)
    inds = range(0, raw_data.shape[0], num_ticks)
    tbs = raw_data.iloc[inds]
    return tbs


def volume_bars(raw_data, num_vol=1000):
    vols = np.cumsum(raw_data['size'])//num_vol
    diff = np.diff(vols, 1)
    diff = np.insert(diff,0,0)
    #print(diff.sum())
    bool_diff = (diff == 1)
    vbs = raw_data.iloc[bool_diff]
    #print(vbs.head())
    return vbs


def dollar_bars(raw_data, num_dollar=1e6):
    dol_cum = np.cumsum(raw_data['dollar_vol'])//num_dollar
    diff = np.diff(dol_cum, 1)
    diff = np.insert(diff, 0, 0)
    bool_diff = (diff == 1)
    dbs = raw_data.iloc[bool_diff]
    #print(dbs.head())
    return dbs


def count_bars_per_week(bars): #count number of bars by week
    count_week = bars.assign(count=1)
    wk_num = count_week['count'].resample('W').sum()
    return wk_num

def scale(s):
    return (s-s.min())/(s.max()-s.min())

def returned(s):
    return pd.Series(np.diff(np.log(s)), index=s.index[1:])



import pandas as pd

raw_file = "IVE_tickbidask.txt"
cols = ['date','time','price','bid','ask','size']
raw_data = pd.read_csv(raw_file, header=None)
raw_data = sample_data(raw_data)
raw_data = (raw_data
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
#plt.plot(tbs_wk)

tbs_wk_scale, vbs_wk_scale, dbs_wk_scale = scale(tbs_wk), scale(vbs_wk), scale(dbs_wk)
#print("scaled weekly counts:", tbs_wk_scale, vbs_wk_scale, dbs_wk_scale)
print("std of scaled weekly counts:", tbs_wk_scale.std(), vbs_wk_scale.std(), dbs_wk_scale.std())

#2.1(c)
tbs_return, vbs_return, dbs_return = returned(tbs['price']), returned(vbs['price']), returned(dbs['price'])
print("std of returns:", tbs_return.std(), vbs_return.std(), dbs_return.std())

#2.1(d)
tbs_mth_return_var, vbs_mth_return_var, dbs_mth_return_var = tbs_return.resample('1M').var(), vbs_return.resample('1M').var(), dbs_return.resample('1M').var()
print("std of mth return:", tbs_mth_return_var, vbs_mth_return_var, dbs_mth_return_var)
print("var of var of mth return:", tbs_mth_return_var.var(), vbs_mth_return_var.var(), dbs_mth_return_var.var())

#2.1(e)
from scipy import stats
print("Jarque-Bera normality test:", stats.jarque_bera(tbs_return.values), stats.jarque_bera(vbs_return.values), stats.jarque_bera(dbs_return.values))


