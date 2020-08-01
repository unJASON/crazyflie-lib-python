import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.position_hl_commander import PositionHlCommander
from cflib.positioning.motion_commander import MotionCommander
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.crazyflie.syncLogger import SyncLogger
import math
import time
import pandas as pd

# URI to the Crazyflie to connect to
# 随机窗口大小为81
# 研究 集群收发包 及 测距 现象
uri1 = "radio://0/10/2M"
mapper_start={}
mapper_finish={}
isFinish = False
rx_data1=['rxCNT.rxcnt10','rxCNT.rxcnt20','rxCNT.rxcnt30','rxCNT.rxcnt40','rxCNT.rxcnt50']
rx_data2=['rxCNT2.rxcnt60','rxCNT2.rxcnt70','rxCNT2.rxcnt80','rxCNT2.rxcnt90']
rg_data1=[
    'rangingCNT.rangingcnt10',
    'rangingCNT.rangingcnt20',
    'rangingCNT.rangingcnt30',
    'rangingCNT.rangingcnt40',
    'rangingCNT.rangingcnt50']
rg_data2=[
    'rangingCNT2.rangingcnt60',
    'rangingCNT2.rangingcnt70',
    'rangingCNT2.rangingcnt80',
    'rangingCNT2.rangingcnt90']
def rxCNT_data(timestamp, data, logconf):
    for ele in rx_data1:
        if not isFinish:
            mapper_start[ele]=data[ele]
            print(logconf.cf.link_uri, mapper_start)
        else:
            mapper_finish[ele]=data[ele]
            print(logconf.cf.link_uri, mapper_finish)
def rxCNT_data2(timestamp, data, logconf):
    for ele in rx_data2:
        if not isFinish:
            mapper_start[ele] = data[ele]
            print(logconf.cf.link_uri, mapper_start)
        else:
            mapper_finish[ele] = data[ele]
            print(logconf.cf.link_uri, mapper_finish)

def ranging_data(timestamp, data, logconf):
    for ele in rg_data1:
        if not isFinish:
            mapper_start[ele] = data[ele]
            print(logconf.cf.link_uri, mapper_start)
        else:
            mapper_finish[ele] = data[ele]
            print(logconf.cf.link_uri, mapper_finish)

def ranging_data2(timestamp, data, logconf):
    for ele in rg_data2:
        if not isFinish:
            mapper_start[ele] = data[ele]
            print(logconf.cf.link_uri, mapper_start)
        else:
            mapper_finish[ele] = data[ele]
            print(logconf.cf.link_uri, mapper_finish)

def distance_measurement(uri):
    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:

        lpos = LogConfig(name='rxCNT', period_in_ms=100)
        for ele in rx_data1:
            lpos.add_variable(ele)
        scf.cf.log.add_config(lpos)
        lpos.data_received_cb.add_callback(rxCNT_data)
        lpos.start()
        time.sleep(1)
        lpos.stop()

        lpos = LogConfig(name='rxCNT', period_in_ms=100)
        for ele in rx_data2:
            lpos.add_variable(ele)
        scf.cf.log.add_config(lpos)
        lpos.data_received_cb.add_callback(rxCNT_data2)
        lpos.start()
        time.sleep(1)
        lpos.stop()

        lpos = LogConfig(name='rxCNT', period_in_ms=100)
        for ele in rg_data1:
            lpos.add_variable(ele)
        scf.cf.log.add_config(lpos)
        lpos.data_received_cb.add_callback(ranging_data)
        lpos.start()
        time.sleep(1)
        lpos.stop()

        lpos = LogConfig(name='rxCNT', period_in_ms=100)
        for ele in rg_data2:
            lpos.add_variable(ele)
        scf.cf.log.add_config(lpos)
        lpos.data_received_cb.add_callback(ranging_data2)
        lpos.start()
        time.sleep(1)
        lpos.stop()

        time.sleep(200)
        global isFinish
        isFinish = True

        #结束
        lpos = LogConfig(name='rxCNT', period_in_ms=100)
        for ele in rx_data1:
            lpos.add_variable(ele)
        scf.cf.log.add_config(lpos)
        lpos.data_received_cb.add_callback(rxCNT_data)
        lpos.start()
        time.sleep(1)
        lpos.stop()

        lpos = LogConfig(name='rxCNT', period_in_ms=100)
        for ele in rx_data2:
            lpos.add_variable(ele)
        scf.cf.log.add_config(lpos)
        lpos.data_received_cb.add_callback(rxCNT_data2)
        lpos.start()
        time.sleep(1)
        lpos.stop()

        lpos = LogConfig(name='rxCNT', period_in_ms=100)
        for ele in rg_data1:
            lpos.add_variable(ele)
        scf.cf.log.add_config(lpos)
        lpos.data_received_cb.add_callback(ranging_data)
        lpos.start()
        time.sleep(1)
        lpos.stop()

        lpos = LogConfig(name='rxCNT', period_in_ms=100)
        for ele in rg_data2:
            lpos.add_variable(ele)
        scf.cf.log.add_config(lpos)
        lpos.data_received_cb.add_callback(ranging_data2)
        lpos.start()
        time.sleep(1)
        lpos.stop()
    dt_col = ['uri']
    dt = [uri]
    for k,v in mapper_finish.items():
        dt_col.append(k)
        dt.append(v-mapper_start[k])
    df = pd.DataFrame([dt], columns=dt_col)
    df.to_csv('./comparison_50ms_3_2.csv', index=False)
    return

if __name__ == '__main__':
    # init drivers mandatory
    cflib.crtp.init_drivers(enable_debug_driver=False)

    distance_measurement(uri1)