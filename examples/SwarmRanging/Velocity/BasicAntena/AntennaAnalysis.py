import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import mean_squared_error,mean_absolute_error
import numpy as np
file_path = [
    # 'antenna_0.1_154.33.csv',
    # 'antenna_0.1_154.33_2.csv',
    # 'antenna_0.1_154.40.csv',
    # 'antenna_0.1_154.40_2.csv',
    # 'antenna_0.1_154.50.csv',
    # 'antenna_0.1_154.50_2.csv',
    # 'antenna_0.1_154.50_3.csv',
    # 'antenna_0.1_154.55.csv',
    # 'antenna_0.1_154.55_2.csv',
    # 'antenna_0.1_154.55_3.csv',
    # 'antenna_0.1_154.60.csv',
    # 'antenna_0.1_154.60_2.csv',
    # 'antenna_0.1_154.60_3.csv',
    # 'antenna_0.1_154.65.csv',
    # 'antenna_0.1_154.65_2.csv',
    # 'antenna_0.1_154.65_3.csv',
    # 'antenna_0.1_154.65_6.csv',
    # 'antenna_0.1_154.65_7.csv',
    # 'antenna_0.1_154.65_8.csv',
    'antenna_0.1_154.70.csv',
    'antenna_0.1_154.70_2.csv',
    'antenna_0.1_154.70_3.csv',
    'antenna_0.1_154.70_6.csv',
    'antenna_0.1_154.70_7.csv',
    'antenna_0.1_154.70_8.csv',
    # 'antenna_0.1_154.72.csv',
    # 'antenna_0.1_154.72_2.csv',
    # 'antenna_0.1_154.72_3.csv',
    # 'antenna_0.1_154.74.csv',
    # 'antenna_0.1_154.74_2.csv',
    # 'antenna_0.1_154.74_3.csv',
    # 'antenna_0.1_154.75.csv',
    # 'antenna_0.1_154.75_2.csv',
    # 'antenna_0.1_154.75_3.csv',
    # 'antenna_0.1_154.75_4.csv',
    # 'antenna_0.1_154.75_5.csv',
    # 'antenna_0.1_154.75_6.csv',
    # 'antenna_0.1_154.76.csv',
    # 'antenna_0.1_154.76_2.csv',
    # 'antenna_0.1_154.76_3.csv',
    # 'antenna_0.1_154.78.csv',
    # 'antenna_0.1_154.78_2.csv',
    # 'antenna_0.1_154.78_3.csv',
    # 'antenna_0.1_154.80.csv',
]
if __name__ == '__main__':
    for ele in file_path:
        vel_file = pd.read_csv(filepath_or_buffer=ele)
        # vel_file=vel_file.iloc[100:,:]
        vel_file = vel_file.loc[:, ['distance_lighthouse', 'distance_UWB']]
        # 去掉离群点
        vel_file = vel_file[vel_file.distance_UWB < 10]
        vel_file = vel_file[vel_file.distance_UWB > 0]
        # 这步关键！！！
        vel_file = vel_file[vel_file.distance_lighthouse > 0.5]
        vel_file = vel_file[vel_file.distance_lighthouse < 3]

        # vel_file=vel_file.iloc[:266,:]
        # print(ele,'MSE',mean_squared_error(vel_file["distance_UWB"],vel_file["distance_lighthouse"]))
        print(ele,'MAE',mean_absolute_error(vel_file["distance_UWB"],vel_file["distance_lighthouse"]))
        plt.figure()
        sns.lineplot(x=[0,4],y=[0,4])
        sns.scatterplot(x='distance_lighthouse',y='distance_UWB',data=vel_file)
        plt.show()
        # plt.figure()
        # sns.relplot(x='distance_lighthouse',y='distance_UWB',kind="line", ci="sd",data=vel_file)
        # plt.show()