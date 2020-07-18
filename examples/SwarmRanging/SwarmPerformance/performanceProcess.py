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

# 研究 集群收发包 及 测距 现象
uri1 = "radio://0/10/2M"
uri2 = "radio://0/20/2M"
uri3 = "radio://0/30/2M"
uri4 = "radio://0/40/2M"
uris = [uri1,uri2,uri3,uri4]
# uris = [uri1,uri2]

dt_mapper={}
dt = []

def pos_data(timestamp, data, logconf):
    position = [
        data['rxCNT.rxcnt10'],
        data['rxCNT.rxcnt20'],
        data['rxCNT.rxcnt30'],
        data['rxCNT.rxcnt40'],
    ]
    print( logconf.cf.link_uri,position )
    if logconf.cf.link_uri not in dt_mapper.keys():
        dt.append((logconf.cf.link_uri,position[0],position[1],position[2],position[3]))
        dt_mapper[logconf.cf.link_uri] = position
    else:
        pass

def pos_data2(timestamp, data, logconf):
    position = [
        data['rangingCNT.rangingcnt10'],
        data['rangingCNT.rangingcnt20'],
        data['rangingCNT.rangingcnt30'],
        data['rangingCNT.rangingcnt40'],
    ]
    print( logconf.cf.link_uri,position )
    if logconf.cf.link_uri not in dt_mapper.keys():
        dt.append((logconf.cf.link_uri,position[0],position[1],position[2],position[3]))
        dt_mapper[logconf.cf.link_uri] = position
    else:
        pass

def distance_measurement():
    for uri in uris:
        with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
            lpos = LogConfig(name='rxCNT', period_in_ms=500)
            lpos.add_variable('rxCNT.rxcnt10')
            lpos.add_variable('rxCNT.rxcnt20')
            lpos.add_variable('rxCNT.rxcnt30')
            lpos.add_variable('rxCNT.rxcnt40')
            scf.cf.log.add_config(lpos)
            lpos.data_received_cb.add_callback(pos_data)
            lpos.start()
            time.sleep(2)
            lpos.stop()
    df = pd.DataFrame(dt, columns=['uri', 'rxcnt10', 'rxcnt20', 'rxcnt30', 'rxcnt40'])
    df.to_csv('./rxcnt.csv', index=False)
    dt.clear()
    dt_mapper.clear()
    for uri in uris:
        with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
            lpos = LogConfig(name='rxCNT', period_in_ms=500)
            lpos.add_variable('rangingCNT.rangingcnt10')
            lpos.add_variable('rangingCNT.rangingcnt20')
            lpos.add_variable('rangingCNT.rangingcnt30')
            lpos.add_variable('rangingCNT.rangingcnt40')
            scf.cf.log.add_config(lpos)
            lpos.data_received_cb.add_callback(pos_data2)
            lpos.start()
            time.sleep(2)
            lpos.stop()
    df = pd.DataFrame(dt, columns=['uri', 'rangingcnt10', 'rangingcnt20', 'rangingcnt30', 'rangingcnt40'])
    df.to_csv('./rangingcnt.csv', index=False)
    print("done")
    return

if __name__ == '__main__':
    # init drivers mandatory
    cflib.crtp.init_drivers(enable_debug_driver=False)

    distance_measurement()