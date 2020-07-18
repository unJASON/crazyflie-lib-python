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

# 研究“死周期” 与 测距周期 、 报文长度 的 关系
uri = "radio://0/40/2M"
dt = []

def pos_data(timestamp, data, logconf):
    position = [
        data['peerdist.distance2peer50'],
    ]
    print( position )
    dt.append((position[0],time.time()))


def distance_measurement():
    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        lpos = LogConfig(name='distance', period_in_ms=10)
        lpos.add_variable('peerdist.distance2peer50')
        scf.cf.log.add_config(lpos)
        lpos.data_received_cb.add_callback(pos_data)
        lpos.start()
        time.sleep(200)
    df = pd.DataFrame(dt,columns=['distance','time'])
    df.to_csv('./dist_99_p10_200s_10_1.csv',index=False)
    print("done")
    return

if __name__ == '__main__':
    # init drivers mandatory
    cflib.crtp.init_drivers(enable_debug_driver=False)

    distance_measurement()