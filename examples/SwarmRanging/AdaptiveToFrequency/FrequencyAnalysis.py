import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
# 研究 测距频率的适应 的 关系

pairs_mapper={
    "distance10":"30ms-30ms",
    "distance20":"30ms-40ms",
    "distance30":"30ms-50ms",
    "distance40":"30ms-60ms",
    "distance50":"30ms-70ms"
}

#记录测距次数
def ranging_cnt(dist):
    dist_dic = {}
    flag_dict = {}
    dist=dist.drop(["time"],axis=1)
    for col in dist.columns:
        dist_dic[col] = []
        flag_dict[col] = -10000000
    for idx,row in dist.iterrows():
        for col in dist.columns:
            if row[col] != flag_dict[col]:
                if len(dist_dic[col]) == 0:
                    dist_dic[col].append(1)
                else:
                    dist_dic[col].append(dist_dic[col][-1]+1)
                flag_dict[col] = row[col]
            else:
                dist_dic[col].append(dist_dic[col][-1])
    for k,v in dist_dic.items():
        print(k,v[-1],max(np.bincount(v)))
    return dist_dic

if __name__ == '__main__':
    data_plt = pd.DataFrame()

    # group test
    dist = pd.read_csv(filepath_or_buffer="./group_test_10203040_40.csv")
    dist_dic = ranging_cnt(dist)
    for k, v in dist_dic.items():
        if k == 'distance10' or k == 'distance50':
            pass
        else:
            temp_df = pd.DataFrame()
            temp_df['ranging counts'] = v
            temp_df['type'] = 'swarm ranging'
            # 重新命名
            temp_df['ranging pairs'] = pairs_mapper[k]
            temp_df['time'] = [i for i in range(len(v))]

            data_plt = pd.concat([data_plt,temp_df],axis=0)
    # pair test
    filepath = [
            "./freq_10_rd41_20_rd41.csv",
            "./freq_10_rd41_30_rd41.csv",
            "./freq_10_rd41_40_rd41.csv",
        ]
    for idx, ele in enumerate(filepath):
        ranging_dt = pd.read_csv(filepath_or_buffer=ele)
        dist_dic = ranging_cnt(ranging_dt)
        k = 'distance' + str((idx + 2) * 10)
        v = dist_dic[k]

        temp_df = pd.DataFrame()
        temp_df['ranging counts'] = v
        temp_df['type'] = 'pair ranging'
        # 重命名
        temp_df['ranging pairs'] = pairs_mapper[k]

        temp_df['time'] = [i for i in range(len(v))]

        data_plt = pd.concat([data_plt,temp_df],axis=0)


    # 画图
    plt.figure()
    sns.lineplot(y='ranging counts',x = 'time',
                 hue='ranging pairs', style='type',data=data_plt)
    plt.show()

    # 分布
    # plt.figure()
    # sns.distplot(test.iloc[:500,0])
    # plt.show()


    #确定测距次数
    # plt.figure()
    # sns.scatterplot(x=list(),y=list())
    # plt.show()