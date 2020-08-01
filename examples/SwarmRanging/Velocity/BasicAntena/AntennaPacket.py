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
import numpy as np
import time
import pandas as pd
#找一个好点的天线延时
#令一台无人机静止另外一台以不同速度远离该无人机
#记录每时每刻的lighthouse位置与测距距离
uri = 'radio://0/10/2M'

distance_mapper={
'radio://0/20/2M':'peerdist.distance2peer20',
'radio://0/30/2M':'peerdist.distance2peer30',
'radio://0/60/2M':'peerdist2.distance2peer60'
}

#固定点的飞机
uri_fixed = 'radio://0/20/2M'
#固定点位置
pos_fixed=[]

fixed_dt=[]
moving_dt=[]
def pos_data(timestamp, data, logconf):
    global pos_fixed
    position = [
        data['stateEstimate.x'],
        data['stateEstimate.y'],
        data['stateEstimate.z'],
        data[distance_mapper[uri_fixed]]
    ]
    distance = 0
    for i in range(3):
        distance = distance + (position[i]-pos_fixed[i])**2
    distance = distance**(0.5)
    position.append(distance)

    print(position)

    moving_dt.append(position)

def pos_data_fixed(timestamp, data, logconf):
    position = [
        data['stateEstimate.x'],
        data['stateEstimate.y'],
        data['stateEstimate.z']
    ]
    print(position)
    fixed_dt.append(position)

def line_sequence(velocity):
    global pos_fixed
    #先记录固定点的坐标用于计算距离
    with SyncCrazyflie(uri_fixed,cf=Crazyflie(rw_cache='./cache')) as scf:
        lpos = LogConfig(name='position',period_in_ms=100)
        lpos.add_variable('stateEstimate.x')
        lpos.add_variable('stateEstimate.y')
        lpos.add_variable('stateEstimate.z')
        scf.cf.log.add_config(lpos)
        lpos.data_received_cb.add_callback(pos_data_fixed)
        lpos.start()
        time.sleep(2)
        lpos.stop()
    pos_fixed = np.mean(fixed_dt, axis=0).tolist()
    print(pos_fixed)

    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        lpos = LogConfig(name='position', period_in_ms=100)
        lpos.add_variable('stateEstimate.x')
        lpos.add_variable('stateEstimate.y')
        lpos.add_variable('stateEstimate.z')
        lpos.add_variable(distance_mapper[uri_fixed])
        scf.cf.log.add_config(lpos)
        lpos.data_received_cb.add_callback(pos_data)
        with PositionHlCommander(scf,default_velocity=velocity) as pc:
            time.sleep(2)
            pc.go_to(2.0, 0.0, 0.5)
            lpos.start()
            pc.go_to(-0.5, 0, 0.5)
            lpos.stop()


    df = pd.DataFrame(moving_dt,columns=['x','y','z','distance_UWB','distance_lighthouse'])
    df.to_csv('./antenna_'+str(velocity)+'_154.65_8'+'.csv',index=False)
if __name__ == '__main__':
    # init drivers mandatory
    cflib.crtp.init_drivers(enable_debug_driver=False)

    line_sequence(0.1)