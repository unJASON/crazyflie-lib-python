import time
import cflib.crtp
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.positioning.position_hl_commander import PositionHlCommander
import pandas as pd
from cflib.positioning.motion_commander import MotionCommander

# Change uris and sequences according to your setup
URI = 'radio://0/10/2M'
URI_fixed = 'radio://0/20/2M'

distance_mapper={
'radio://0/20/2M':'peerdist.distance2peer20',
'radio://0/30/2M':'peerdist.distance2peer30',
'radio://0/60/2M':'peerdist2.distance2peer60'
}
vel = 0.5
#    x   y   z  time
sequence1 = [
    (-0.8, 0, 0.5, 3.0),
    (1.2, 0, 0.5, 3.0),
    (-0.8, 0, 0.5, 3.0),
]
sequence2 = [
    (2.2, 0, 0.5, 20),
]

seq_args = {
    URI: [sequence1],
    URI_fixed: [sequence2],
}
# List of URIs, comment the one you do not want to fly
uris = {
    URI,
    URI_fixed,
}
moving_dt =[]

def pos_data(timestamp, data, logconf):
    position = [
        data['stateEstimate.x'],
        data['stateEstimate.y'],
        data['stateEstimate.z'],
        data[distance_mapper[URI_fixed]]
    ]
    distance = 0
    for i in range(3):
        distance = distance + (position[i] - sequence2[0][i]) ** 2
    distance = distance ** (0.5)
    position.append(distance)
    print(position)

    moving_dt.append(position)
    return

def pos_data_fixed(timestamp, data, logconf):
    position = [
        data['stateEstimate.x'],
        data['stateEstimate.y'],
        data['stateEstimate.z']
    ]
    print(position)
    return
def wait_for_param_download(scf):
    while not scf.cf.param.is_updated:
        time.sleep(1.0)
    print('Parameters downloaded for', scf.cf.link_uri)

def run_sequence(scf, sequence):
    try:
        cf = scf.cf
        lpos = LogConfig(name='position', period_in_ms=60)
        lpos.add_variable('stateEstimate.x')
        lpos.add_variable('stateEstimate.y')
        lpos.add_variable('stateEstimate.z')
        # 配置
        if scf.cf.link_uri == URI:
            lpos.add_variable(distance_mapper[URI_fixed])
        else:
            pass
        scf.cf.log.add_config(lpos)

        # 回调
        if scf.cf.link_uri == URI:
            lpos.data_received_cb.add_callback(pos_data)
        else:
            lpos.data_received_cb.add_callback(pos_data_fixed)
        # lpos.start()
        # time.sleep(500)
        # lpos.stop()

        with PositionHlCommander(scf) as pc:
            if scf.cf.link_uri == URI:
                pc.set_default_velocity(vel)
                # 等待二号无人机飞到指定地点后开始做事情
                pc.go_to(sequence[0][0],sequence[0][1],sequence[0][2])
                time.sleep(5)
                lpos.start()
                for ele in sequence:
                    pc.go_to(ele[0],ele[1],ele[2])
                lpos.stop()
            else:
                for ele in sequence:
                    pc.go_to(ele[0],ele[1],ele[2])
                    time.sleep(ele[3])

        if scf.cf.link_uri == URI:
            df = pd.DataFrame(moving_dt,columns=['x','y','z','distance_UWB','distance_lighthouse'])
            df.to_csv('./Swarm_'+str(vel)+'_200ms_2.csv',index=False)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    cflib.crtp.init_drivers(enable_debug_driver=False)

    factory = CachedCfFactory(rw_cache='./cache')
    with Swarm(uris, factory=factory) as swarm:
        # The current values of all parameters are downloaded as a part of the
        # connections sequence. Since we have 10 copters this is clogging up
        # communication and we have to wait for it to finish before we start
        # flying.
        print('Waiting for parameters to be downloaded...')
        swarm.parallel(wait_for_param_download)

        swarm.parallel(run_sequence, args_dict=seq_args)
