import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import mean_squared_error,mean_absolute_error
import numpy as np
file_path = [
    'VelocitySwarm_50ms_0.1.csv',
    'VelocitySwarm_50ms_0.5.csv',
    'VelocitySwarm_50ms_0.1_far.csv',
    'VelocitySwarm_50ms_0.5_far.csv',

]
if __name__ == '__main__':
    for ele in file_path:
        vel_file = pd.read_csv(filepath_or_buffer=ele)
        # vel_file=vel_file.iloc[100:,:]
        vel_file = vel_file.loc[:,['distance_lighthouse','distance_UWB']]
        #去掉离群点
        vel_file = vel_file[vel_file.distance_UWB <10]
        #这步关键！！！
        vel_file = vel_file[vel_file.distance_lighthouse > 1 ]
        vel_file = vel_file[vel_file.distance_lighthouse < 3]

        # print(ele,'MSE',mean_squared_error(vel_file["distance_UWB"],vel_file["distance_lighthouse"]))
        print(ele,vel_file.shape[0],'MAE',mean_absolute_error(vel_file["distance_UWB"],vel_file["distance_lighthouse"]))
        # plt.figure()
        # sns.lineplot(x=[0,4],y=[0,4])
        # sns.scatterplot(x='distance_lighthouse',y='distance_UWB',data=vel_file)
        # plt.show()
        plt.figure()
        gt_dt = pd.DataFrame(columns=vel_file.columns)
        #画groundtruth
        gt_dt['distance_lighthouse'] = vel_file['distance_lighthouse']
        gt_dt['distance_UWB'] = vel_file['distance_lighthouse']
        gt_dt['data'] = 'ground truth'
        vel_file['data']= ele
        vel_file = pd.concat([vel_file,gt_dt],axis=0)
        sns.relplot(x='distance_lighthouse',y='distance_UWB',kind="line",hue='data',data=vel_file)
        plt.show()