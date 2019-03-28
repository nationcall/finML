# define functions to generate bars


def tick_bars(raw_data, num_ticks=1000):
    '''
    :param raw_data: time bars
    :return: tick bars
    '''
    #inds = range(0, 10000, 1000)
    inds = range(0, raw_data.shape[0], num_ticks)
    tbs = raw_data.loc[inds]
    return tbs

def volume_bars(raw_data, num_vol=1000):
    


import pandas as pd

raw_file = "IVE_tickbidask.txt"
cols = ['date','time','price','bid','ask','size']
raw_data = (pd.read_csv(raw_file,nrows=5000,header=None)
            .rename(columns=dict(zip(range(len(cols)),cols))))
raw_data.head()
tick_bars(raw_data)