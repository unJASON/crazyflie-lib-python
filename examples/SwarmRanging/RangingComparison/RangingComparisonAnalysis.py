import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
mapper={}
mapper["50ms"]=[
'./comparison_50ms_2.csv',
'./comparison_50ms_3.csv',
'./comparison_50ms_4.csv',
'./comparison_50ms_5.csv',
'./comparison_50ms_6.csv',
'./comparison_50ms_7.csv',
'./comparison_50ms_8.csv',
'./comparison_50ms_9.csv',
]
mapper["100ms"]=[
'./comparison_100ms_2.csv',
'./comparison_100ms_3.csv',
'./comparison_100ms_4.csv',
'./comparison_100ms_5.csv',
'./comparison_100ms_6.csv',
'./comparison_100ms_7.csv',
'./comparison_100ms_8.csv',
'./comparison_100ms_9.csv',

]
mapper["150ms"]=[
'./comparison_150ms_2.csv',
'./comparison_150ms_3.csv',
'./comparison_150ms_4.csv',
'./comparison_150ms_5.csv',
'./comparison_150ms_6.csv',
'./comparison_150ms_7.csv',
'./comparison_150ms_8.csv',
'./comparison_150ms_9.csv',
]

rg_cnt_li = ['rangingCNT.rangingcnt10',
             'rangingCNT.rangingcnt20',
             'rangingCNT.rangingcnt30',
             'rangingCNT.rangingcnt40',
             'rangingCNT.rangingcnt50',
             'rangingCNT2.rangingcnt60',
             'rangingCNT2.rangingcnt70',
             'rangingCNT2.rangingcnt80',
             'rangingCNT2.rangingcnt90'
             ]


if __name__ == '__main__':
    line_mapper = {}
    for k, v in mapper.items():
        line_mapper[k] = []
        for idx,ele in enumerate(v):
            rang_cnt = pd.read_csv(filepath_or_buffer=ele)
            nums = 0
            for idx,rows in rang_cnt.iterrows():
                for rg_col in rg_cnt_li:
                    nums = nums + rows[rg_col]
            line_mapper[k].append(nums)
    plt.figure()
    for k,v in line_mapper.items():
        sns.lineplot(x=[i for i in range(2,len(v)+2)],y=v)
    plt.show()