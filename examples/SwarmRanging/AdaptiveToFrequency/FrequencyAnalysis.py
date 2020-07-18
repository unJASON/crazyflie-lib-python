import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
# 研究 集群测距的频率的适应 的 关系


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

    dist = pd.read_csv(filepath_or_buffer="./group_test_10203040_40.csv")
    dist_dic=ranging_cnt(dist)
    # 折线
    plt.figure()
    for k,v in dist_dic.items():
        sns.lineplot(y=v, x=[i for i in range(len(v))])
    plt.show()

    # 分布
    # plt.figure()
    # sns.distplot(test.iloc[:500,0])
    # plt.show()


    #确定测距次数
    # plt.figure()
    # sns.scatterplot(x=list(),y=list())
    # plt.show()