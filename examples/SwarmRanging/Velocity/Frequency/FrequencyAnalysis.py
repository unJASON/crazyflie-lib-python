import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import mean_squared_error,mean_absolute_error
import numpy as np
file_path = [
    # 'Swarm_0.3_15ms.csv',
    # 'Swarm_0.4_15ms.csv',
    # 'Swarm_0.5_15ms.csv',
    #
    # 'Swarm_0.3_50ms.csv',
    # 'Swarm_0.4_50ms.csv',
    # 'Swarm_0.5_50ms.csv',

    # 'Swarm_0.3_100ms.csv',
    # 'Swarm_0.4_100ms.csv',
    # 'Swarm_0.5_100ms.csv',

    # 'Swarm_0.3_150ms.csv',
    # 'Swarm_0.4_150ms.csv',
    # 'Swarm_0.5_150ms.csv',

    'Swarm_0.3_200ms.csv',
    'Swarm_0.4_200ms.csv',
    'Swarm_0.5_200ms.csv',
    'Swarm_0.5_200ms_2.csv',
]
if __name__ == '__main__':
    for ele in file_path:
        vel_file = pd.read_csv(filepath_or_buffer=ele)
        # vel_file=vel_file.iloc[100:,:]
        vel_file = vel_file.loc[:,['distance_lighthouse','distance_UWB']]
        #去掉离群点
        vel_file = vel_file[vel_file.distance_UWB <10]
        #这步关键！！！
        # vel_file = vel_file[vel_file.distance_lighthouse>0.3]

        # print(ele,'MSE',mean_squared_error(vel_file["distance_UWB"],vel_file["distance_lighthouse"]))
        print(ele,'MAE',mean_absolute_error(vel_file["distance_UWB"],vel_file["distance_lighthouse"]))
        # plt.figure()
        # sns.lineplot(x=[i for i in range(vel_file.shape[0])],y='distance_UWB',data=vel_file)
        # sns.lineplot(x=[i for i in range(vel_file.shape[0])],y='distance_lighthouse',data=vel_file)
        # plt.show()
        # plt.figure()
        # sns.scatterplot(x=[i for i in range(vel_file.shape[0])], y='distance_UWB', data=vel_file)
        # sns.scatterplot(x=[i for i in range(vel_file.shape[0])], y='distance_lighthouse', data=vel_file)
        # plt.show()
        # plt.figure()
        # gt_dt = pd.DataFrame(columns=vel_file.columns)
        # #画groundtruth
        # gt_dt['distance_lighthouse'] = vel_file['distance_lighthouse']
        # gt_dt['distance_UWB'] = vel_file['distance_lighthouse']
        # gt_dt['data'] = 'lighthouse'
        # vel_file['data']= ele
        # vel_file = pd.concat([vel_file,gt_dt],axis=0)
        # sns.relplot(x='distance_lighthouse',y='distance_UWB',kind="line",hue='data',data=vel_file)
        # plt.show()


    plt.figure()
    li =[50,150]
    file_str = 'Swarm_0.5_'
    for idx,ele in enumerate(li):
        file_str_tmp = file_str+str(ele)+'ms'+'.csv'
        vel_file = pd.read_csv(filepath_or_buffer=file_str_tmp)
        sns.lineplot(x=[i for i in range(vel_file.shape[0])],y='distance_UWB',data=vel_file)
    vel_file = pd.read_csv(filepath_or_buffer=file_str+str(li[0])+'ms'+'.csv')
    sns.lineplot(x=[i for i in range(vel_file.shape[0])],y='distance_lighthouse',data=vel_file)
    plt.show()