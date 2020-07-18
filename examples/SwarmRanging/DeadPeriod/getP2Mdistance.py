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
uri = 'radio://0/10/2M'
uri2 = 'radio://0/50/2M'
dt = []
def pos_data(timestamp, data, logconf):
    position = [
        data['peerdist.distance2peer10'],
        data['peerdist.distance2peer20'],
        data['peerdist.distance2peer30'],
        data['peerdist.distance2peer40']
    ]
    print(logconf.name, position )
    dt.append((position[0],position[1],position[2],position[3]))
def distance_measurement():
    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        lpos = LogConfig(name='Position', period_in_ms=300)
        lpos.add_variable('peerdist.distance2peer10')
        lpos.add_variable('peerdist.distance2peer20')
        lpos.add_variable('peerdist.distance2peer30')
        lpos.add_variable('peerdist.distance2peer40')
        scf.cf.log.add_config(lpos)
        lpos.data_received_cb.add_callback(pos_data)
        lpos.start()
        time.sleep(300)
    # df = pd.DataFrame(dt,columns=['d1','d2','d3','d4'])
    # df.to_csv('./dist2Many.csv',index=False)
    print("done")
    return
if __name__ == '__main__':
    cflib.crtp.init_drivers(enable_debug_driver=False)

    # a swarm of UAV
    # coordinate()
    # ==================

    #single UAV
    distance_measurement()
