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

# 研究 集群测距的频率的适应 的 关系
uri = "radio://0/10/2M"
dt = []

def pos_data(timestamp, data, logconf):
    position = [
        data['peerdist.distance2peer10'],
        data['peerdist.distance2peer20'],
        data['peerdist.distance2peer30'],
        data['peerdist.distance2peer40'],
        data['peerdist.distance2peer50']
    ]
    print( position )
    dt.append((position[0],position[1],position[2],position[3],position[4],time.time()))


def distance_measurement():
    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        lpos = LogConfig(name='distance', period_in_ms=10)
        lpos.add_variable('peerdist.distance2peer10')
        lpos.add_variable('peerdist.distance2peer20')
        lpos.add_variable('peerdist.distance2peer30')
        lpos.add_variable('peerdist.distance2peer40')
        lpos.add_variable('peerdist.distance2peer50')
        scf.cf.log.add_config(lpos)
        lpos.data_received_cb.add_callback(pos_data)
        lpos.start()
        time.sleep(200)
    df = pd.DataFrame(dt,columns=['distance10','distance20','distance30','distance40','distance50','time'])
    df.to_csv('./freq_10_rd41_40_rd41.csv',index=False)
    print("done")
    return

def pos_data_cnt(timestamp, data, logconf):
    position = [
        data['rangingCNT.rangingcnt10'],
        data['rangingCNT.rangingcnt20'],
        data['rangingCNT.rangingcnt30'],
        data['rangingCNT.rangingcnt40'],
        data['rangingCNT.rangingcnt50'],
    ]
    print( position )
    dt.append((position[0],position[1],position[2],position[3],position[4],time.time()))


# def distance_measurement_CNT():
#     with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
#         lpos = LogConfig(name='distance', period_in_ms=10)
#         lpos.add_variable('rangingCNT.rangingcnt10')
#         lpos.add_variable('rangingCNT.rangingcnt20')
#         lpos.add_variable('rangingCNT.rangingcnt30')
#         lpos.add_variable('rangingCNT.rangingcnt40')
#         lpos.add_variable('rangingCNT.rangingcnt50')
#         scf.cf.log.add_config(lpos)
#         lpos.data_received_cb.add_callback(pos_data_cnt)
#         lpos.start()
#         time.sleep(200)
#     df = pd.DataFrame(dt,columns=['distance10','distance20','distance30','distance40','distance50','time'])
#     df.to_csv('./group_test_10203040_40_CNT.csv',index=False)
#     print("done")
#     return

if __name__ == '__main__':
    # init drivers mandatory
    cflib.crtp.init_drivers(enable_debug_driver=False)

    distance_measurement()
    # distance_measurement_CNT()