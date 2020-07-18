import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

#分析死周期的间隔情况
def analysise_dead_period(dist):
    dead_period_kv = {}
    dead_period_list=[]
    distance = dist['distance']
    check = distance[0]
    flag = 1
    for idx, ele in enumerate(distance):
        if idx == 0:
            pass
        else:
            if ele == check:
                flag = flag + 1
            else:
                if flag in dead_period_kv.keys():
                    dead_period_kv[flag] += 1
                else:
                    dead_period_kv[flag] = 1
                dead_period_list.append(flag)
                check = ele
                flag = 1
    return dead_period_kv,dead_period_list

#分析测距周期的分布情况
def analysise_ranging_period(dist,dead_period):
    dead_period_idx_kv={}
    distance = dist['distance']
    check = distance[0]
    flag = 1
    for idx, ele in enumerate(distance):
        if idx == 0:
            pass
        else:
            if ele == check:
                flag = flag + 1
            else:
                if flag >= dead_period:
                    dead_period_idx_kv[idx]=flag
                check = ele
                flag = 1
    ranging_period_kv = {}
    raning_period_list = []
    flag_idx = 0
    for k,v in dead_period_idx_kv.items():
        raning_period = k-v - flag_idx
        if raning_period in ranging_period_kv:
            ranging_period_kv[raning_period] += 1
        else:
            ranging_period_kv[raning_period] = 1
        raning_period_list.append(raning_period)
        flag_idx = k

    return ranging_period_kv,raning_period_list

if __name__ == '__main__':

    dist = pd.read_csv(filepath_or_buffer="./dist_99_p10_200s_10_1.csv")
    # 折线
    # plt.figure()
    # sns.lineplot(y=test.iloc[:100, 0], x=[i for i in range(100)])
    # plt.show()

    # 分布
    # plt.figure()
    # sns.distplot(test.iloc[:500,0])
    # plt.show()


    dead_period_kv,dead_period_list = analysise_dead_period(dist)
    #确定死周期的下界
    plt.figure()
    sns.scatterplot(x=list(dead_period_kv.keys()),y=list(dead_period_kv.values()))
    plt.show()
    #死周期下界
    dead_period_flag = 40

    #查看死周期的出现次数
    plt.figure()
    x_list = []
    y_list = []

    for k,v in dead_period_kv.items():
        if k >= dead_period_flag:
            x_list.append(k)
            y_list.append(v)
        else:
            pass
    sns.scatterplot(x=x_list, y=y_list)
    plt.show()

    #查看死周期的分布情况
    plt.figure()
    dist_list=[]
    for ele in dead_period_list:
        if ele >=dead_period_flag:
            dist_list.append(ele)
    dist_list.sort()
    sns.distplot(dist_list)
    plt.show()


    #根据得到的死周期，分析 连续测距周期 的分布情况
    ranging_period_kv,raning_period_list=analysise_ranging_period(dist,dead_period_flag)

    #连续测距周期的次数
    plt.figure()
    sns.scatterplot(x=list(ranging_period_kv.keys()), y=list(ranging_period_kv.values()))
    plt.show()
    #连续测距周期的分布
    plt.figure()
    sns.distplot(raning_period_list)
    plt.show()

    print("Conflicting period mean,var：",np.mean(dist_list),",",np.var(dist_list))
    print("ranging period mean,var:",np.mean(raning_period_list),",",np.var(raning_period_list))
    # 剔除离群点
    ranging_period_list_temp = [x for x in raning_period_list if x >200 ]
    print("离群后 ranging period mean,var:",np.mean(ranging_period_list_temp),",",np.var(ranging_period_list_temp))