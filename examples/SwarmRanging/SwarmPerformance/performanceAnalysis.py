import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
# 集群收发包 情况 及 测距 情况 统计
uri1 = "radio://0/10/2M"
uri2 = "radio://0/20/2M"
uri3 = "radio://0/30/2M"
uri4 = "radio://0/40/2M"
rxmapper ={
    "rxcnt10":uri1,
    "rxcnt20":uri2,
    "rxcnt30":uri3,
    "rxcnt40":uri4
}
rangingmapper={
'rangingcnt10':uri1,
'rangingcnt20':uri2,
'rangingcnt30':uri3,
'rangingcnt40':uri4
}
dt_mapper={}
#记录 收包 测距次数 并输出
def performance_cnt(rangingcnt,rxcnt):
    for idx,row in rxcnt.iterrows():
        for col in rxcnt.columns:
            if col == 'uri':
                pass
            else:
                ss = row['uri']+","+ rxmapper[col]
                if ss not in dt_mapper.keys():
                    dt_mapper[ss] = []
                else:
                    pass
                dt_mapper[ss].append(row[col])
    for idx,row in rangingcnt.iterrows():
        for col in rangingcnt.columns:
            if col == 'uri':
                pass
            else:
                ss = row['uri']+','+ rangingmapper[col]
                if ss not in dt_mapper.keys():
                    dt_mapper[ss] = []
                else:
                    pass
                dt_mapper[ss].append(row[col])
    dt_li = []
    for k,v in dt_mapper.items():
        v.insert(0,k)
        dt_li.append(v)
    return dt_li

if __name__ == '__main__':

    rangingcnt = pd.read_csv(filepath_or_buffer="./rangingcnt.csv")
    rxcnt=pd.read_csv(filepath_or_buffer="./rxcnt.csv")
    dt_li=performance_cnt(rangingcnt,rxcnt)
    df = pd.DataFrame(dt_li, columns=['uris', 'rxCnt','rangingCnt'])
    df.to_csv('./performanceAnalysis.csv', index=False)
    print("done")