import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

filepath=[
    './latency_25ms_50cm.csv',
    './latency_25ms_100cm.csv',
    './latency_25ms_150cm.csv',
    './latency_25ms_200cm.csv',
    './latency_25ms_250cm.csv',
    './latency_25ms_300cm.csv',

    './latency_50ms_50cm.csv',
    './latency_50ms_100cm.csv',
    './latency_50ms_150cm.csv',
    './latency_50ms_200cm.csv',
    './latency_50ms_250cm.csv',
    './latency_50ms_300cm.csv',

    './latency_75ms_50cm.csv',
    './latency_75ms_100cm.csv',
    './latency_75ms_150cm.csv',
    './latency_75ms_200cm.csv',
    './latency_75ms_250cm.csv',
    './latency_75ms_300cm.csv',

    './latency_100ms_50cm.csv',
    './latency_100ms_100cm.csv',
    './latency_100ms_150cm.csv',
    './latency_100ms_200cm.csv',
    './latency_100ms_250cm.csv',
    './latency_100ms_300cm.csv',
]

def pre_data(data):
    data_li = []
    check = -1
    data_mean = data.mean()
    for ele in data:
        if ele == check:
            pass
        else:
            #去掉离群的点
            if np.fabs(ele - data_mean) <0.3:
                data_li.append(ele)
            check = ele
    print(len(data_li),len(data))
    return data_li

if __name__ == '__main__':
    df = pd.DataFrame()
    for ele in filepath:

        ranging_dt = pd.read_csv(filepath_or_buffer=ele)
        ele_array = ele.split('_')
        ranging_dt['period(ms)'] = float(ele_array[1][:-2])
        ele_array[2] = str(float(ele_array[2][:-6])/100) + 'm'

        ranging_dt['ground truth'] = ele_array[2]
        ranging_dt=ranging_dt.drop(['time'],axis=1)

        ranging_dt.rename(columns={'distance':'distance(m)'},inplace=True)

        # ranging_dt['distance(m)'] = ranging_dt['distance(m)']*100

        df =pd.concat([df,ranging_dt],axis=0)

    # plt.figure()
    # sns.catplot(x="period(ms)",y="distance(m)",hue="ground truth",kind="bar",data=df)
    # plt.show()
    # plt.figure()
    # sns.catplot(x="period(ms)", y="distance(m)", hue="ground truth", kind="point", data=df)
    # plt.show()

    # 画分布子图
    col_num = 4
    row_num = 6
    fig,axes = plt.subplots(row_num,col_num,figsize=(16,13))
    for idx,ele in enumerate(filepath):
        ranging_dt = pd.read_csv(filepath_or_buffer=ele)
        # ranging_dt.rename(columns={'distance':'distance(m)'},inplace=True)
        data_li=pre_data(ranging_dt['distance'])
        sns.distplot(data_li,ax=axes[idx%row_num,idx//row_num])
    # plt.tight_layout()
    plt.show()

