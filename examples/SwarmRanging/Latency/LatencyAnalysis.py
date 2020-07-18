import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

filepath=[
    './latency_50ms_50cm.csv',
    './latency_50ms_100cm.csv',
    './latency_50ms_150cm.csv',
    './latency_50ms_200cm.csv',
    './latency_50ms_250cm.csv',
    './latency_50ms_300cm.csv',

    './latency_100ms_50cm.csv',
    './latency_100ms_100cm.csv',
    './latency_100ms_150cm.csv',
    './latency_100ms_200cm.csv',
    './latency_100ms_250cm.csv',
    './latency_100ms_300cm.csv',
]


if __name__ == '__main__':
    ranging_dt = pd.read_csv(filepath_or_buffer='./latency_100ms_300cm.csv')

    plt.figure()
    sns.distplot(ranging_dt.iloc[:, 0])
    plt.show()

    print(np.mean(ranging_dt.iloc[:, 0]))