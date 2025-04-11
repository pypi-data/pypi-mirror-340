from enum import Enum
from shared.base.common import PropertyDefinition
from shared.base.redis_db import redis_service

class DCFXStatusCode(Enum):
    Production_State = 1000
    Standby = 1100
    Pre_Process = 1210 # InterProcess: 1200
    Post_Process = 1220 # InterProcess: 1200
    Block = 1300
    Utilize = 1400
    Unexpected_Loss = 2000
    P_Error_Block = 2100
    Q_Error_Block = 2200
    M_Error_Block = 2300
    Safety_Block = 2400
    Production_Preparation = 3000
    Device_Online = 3100
    Modification = 3200
    Materials_Supply = 3300
    Tools_Change = 3400
    Change_Line = 3500
    Offline_Preparation = 3600
    Scheduled_Downtime = 4000
    Maintenance = 4100
    Non_Production_Use = 4230
    Repair = 4300
    Non_Scheduled = 5000
    Non_Scheduled_Down = 5100
    Non_Scheduled_Online = 5200

class WorkStatusCode(Enum):
    Offline = 0
    Ready = 1
    Error = 2
    Working = 3
    Changing = 4

class PowerStatusCode(Enum):
    Off = 0
    On = 1

class BaseDeviceProps:
    '''
    The property and default value of BaseDevice class, the value of the enum element could be 
    # ! ONLY FOR DEFAULT VALUE SETTING OR COMPARISON
    '''
    # location
    factory = PropertyDefinition(name='factory', type=dict, value={})
    production_factory = PropertyDefinition(name='production_factory', type=dict, value={})
    line = PropertyDefinition(name='line', type=dict, value={})
    section = PropertyDefinition(name='section', type=str, value='')
    group = PropertyDefinition(name='group', type=str, value='')
    station = PropertyDefinition(name='station', type=str, value='')
    # identification
    id = PropertyDefinition(name='id', type=str, value='')
    alias = PropertyDefinition(name='alias', type=str, value='')
    # lane_id = PropertyDefinition(name='lane_id', type=str, value='')
    # absolute device order
    index = PropertyDefinition(name='index', type=int, value=0)
    type = PropertyDefinition(name='type', type=str, value='')
    icon_url = PropertyDefinition(name='icon_url', type=str, value='')
    equipment_model = PropertyDefinition(name='equipment_model', type=str, value='')
    # relative device order
    prev_device_name = PropertyDefinition(name='prev_device_name', type=str, value='')
    next_device_name = PropertyDefinition(name='next_device_name', type=str, value='')
    # status
    working_status_code = PropertyDefinition(name='working_status_code', type=int, value=WorkStatusCode.Offline.value)
    # cfx_code = PropertyDefinition(name='cfx_code', type=int, value=DCFXStatusCode.Non_Scheduled.value)
    power_status_code = PropertyDefinition(name='power_status_code', type=int, value=PowerStatusCode.Off.value)
   

class BaseDevice:
    '''
    The class handle basic device information with redis interactions
    '''
    def __init__(self, device_key: str, service_name: str, props: dict, re_init: bool=False, **kwargs) -> None:
        prop_dict = {}
        for k, v in props.items():
            prop_dict[k] = kwargs.get(k) or v
        
        # initialize redis instances
        self.device_key = device_key
        self.service_name = service_name
        redis_service.init_hash(
            name=f'{self.service_name}:{self.device_key}', 
            init_value=prop_dict, re_init=re_init)
    
    def get_device_dict(self) -> dict[str: dict]:
        return redis_service.get_hash_dict(name=f'{self.service_name}:{self.device_key}')

    def get_device_attr(self, key:str, type_func=None) -> str:
        return redis_service.get_hash_value(name=f'{self.service_name}:{self.device_key}', key=key, type_func=type_func)

    def update_device_attr(self, prop_dict: dict) -> None:
        redis_service.update_hash(name=f'{self.service_name}:{self.device_key}', update_dict=prop_dict)
        msg = f'Updated device [{self.device_key}] property: {prop_dict}'
        print(msg)

    @staticmethod
    def query_devices_keys(service_name: str, query_dict: dict={}) -> set:
        '''
        search keys of given service's device by query_dict
        params: 
        - service_name: service name as prefix of redis e.g. device-info
        - query_dict: condition dict [prop: value]
            - in device-info:
                line: line of a device; will ignore if value in [None, '']
                device_id: id of a device; will ignore if value in [None, '']
                status_code: status code of a device (refer to DCFXStatusCode); will ignore if value is -1
                work_status_code: work status code of a device (refer to WorkStatusCode); will ignore if value is -1
                power_status_code: power status code of a device (refer to PowerStatusCode); will ignore if value is -1
        '''
        selected_query_dict = dict()
        for k, v in query_dict.items():
            if v not in [None, '', -1]:
                selected_query_dict[k] = v
        return redis_service.query_hashes_keys(prefix=service_name, query_dict=selected_query_dict)

    @staticmethod
    def query_devices(service_name: str, query_dict: dict={}, remove_prefix=False) -> dict[str: dict]:
        '''
        search device of given service by query_dict
        params: 
        - service_name: service name as prefix of redis e.g. device-info
        - query_dict: condition dict [prop: value]
            - in device-info:
                line: line of a device; will ignore if value in [None, '']
                device_id: id of a device; will ignore if value in [None, '']
                status_code: status code of a device (refer to DCFXStatusCode); will ignore if value is -1
                work_status_code: work status code of a device (refer to WorkStatusCode); will ignore if value is -1
                power_status_code: power status code of a device (refer to PowerStatusCode); will ignore if value is -1
        '''
        redis_keys = BaseDevice.query_devices_keys(service_name, query_dict)
        result_dict = dict()
        for redis_key in redis_keys:
            key = str(redis_key.split(':')[-1]) if remove_prefix else redis_key
            result_dict[key] = redis_service.get_hash_dict(redis_key)
        return result_dict
        
    @staticmethod
    def create_device_key(line: str, device_id: str, lane_id: str='0') -> str:
        return '{0}.{1}.{2}'.format(line, device_id, lane_id)

if __name__ == '__main__':
    print(f'StatusCode.Block.name: {DCFXStatusCode.Block.name}') # Block
    print(f'StatusCode.Block.value: {DCFXStatusCode.Block.value}') # 1500
    print(f'StatusCode(0).name: {DCFXStatusCode(1500).name}') # Block
    equipment = BaseDevice(factory='f', line='l', section='s', group='g', station='st', equipment_code='test-01', equipment_desc='test_equipment', seq_index=0)
    update_dict = {
            'lane_id': '811', 
            'device_id': 'updated_equip_id',
            'device_n': 'updated_equip_name'
        }
    equipment.update_device_attr(update_dict)
    lane_id = redis_service.get_hash_value(name=f'device-info:{equipment.device_key}', key='lane_id')
    print(f'equipment.lane_id: {lane_id}')
    device_id = equipment.__getattribute__('device_id') if hasattr(equipment, 'device_id') else 'blabla'
    print(f'equipment.device_id: {device_id}')
    device_n = equipment.__getattribute__('device_n') if hasattr(equipment, 'device_n') else 'blabla'
    print(f'equipment.device_n: {device_n}')
    print('Test get_status_code():', equipment.get_status_code()=='Non_Scheduled')
    print('Test get_power_status():', equipment.get_power_status()=='Offline')

    print(BaseDevice.query_devices_keys(service_name='device-info'))
    print('\nLine-S04:',BaseDevice.query_devices_keys(service_name='device-info', query_dict={'line':'S04'}))

    print(len(BaseDevice.query_devices(service_name='device-info', remove_prefix=True)))
    print(len(BaseDevice.query_devices(service_name='device-info', query_dict={'line': 'S05', 'work_status_code':0}, remove_prefix=True)))