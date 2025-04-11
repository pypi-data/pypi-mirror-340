import json
from datetime import datetime
import re
from typing import Callable
from base.config import ServiceEnvSettings

class BaseMQTTMessage:
    '''
    a basic MQTT message class that can load topic and payload
    '''
    def __init__(self, msg) -> None:
        self.topic = msg.topic
        self.payload = msg.payload
        self.decoded = False

        '''
        if msg is a BaseMQTTMessage instance then just assign attrs, 
        but isinstance return False if the instance refer to different path of class, 
        use hasattr to resolve this problem
        '''
        # if isinstance(msg, BaseMQTTMessage):
        if hasattr(msg, 'decoded'):
            self.decoded = msg.decoded
        else:
            # decode payload into json object
            try: 
                payload = self.payload.decode('utf-8')
                self.payload = json.loads(payload)
                self.decoded = True
            except Exception as e:
                self.payload = {
                    'flag': False,
                    'data': [],
                    'message': f'payload load fail: {e}'
                }

    def handle_msg(self, handler: Callable, **kwargs):
        handler(self, **kwargs)

    def match_msg_topic(self, rule: str):
        '''
        evaluate whether a mqtt message matches the given topic rule
        '''
        rule = rule.replace('+', r'[^/]+')
        rule = rule.replace('#', r'.*')
        regex = re.compile('^' + rule + '$')
        return bool(regex.match(self.topic))

class DCFXMessage(BaseMQTTMessage):
    def __init__(self, msg, **kwargs) -> None:
        super().__init__(msg=msg, **kwargs)

        elems = self.topic.split('/')
        # [0] = UsageMode
        # [1] = Area
        self.factory = elems[1]
        # [2] = Line
        self.line = elems[2]
        # [3] = Equipment
        self.device_id = elems[3]
        # [4] = Lane
        self.lane_id = elems[4]
        # [5] = Function
        self.function = elems[5]
        # [6] = MessageName
        self.msg_name = elems[6]
        
        self.device_key = f'{self.line}.{self.device_id}.{self.lane_id}'
        self.now = datetime.now()
        
    @staticmethod
    def create_dcfx_topic(factory: str, line: str, device_id: str, lane_id: str, 
                          function: str, cfx_type: str, cfx_topic: str):
        '''
        依訊息類型建立訊息主題
        '''
        mode = ServiceEnvSettings.SERVICE_MODE
        if not lane_id: lane_id = '0'
        msg_name = f'CFX.{cfx_type}.{cfx_topic}' if cfx_type else f'CFX.{cfx_topic}'
        topic = f'{mode}/{factory}/{line}/{device_id}/{lane_id}/{function}/{msg_name}'
        
        return topic
    
    
class BaseAMQPMessage:
    
    def __init__(self, msg) -> None:
        self.msg = msg
        self.decoded = False
        self.message_name = ""
        self.device_name = ""
        try:
            self.message_name = msg["MessageName"]
            # self.device_name = msg["Source"].split(".")[2]
            self.device_name = msg["Source"]
            # if isinstance(msg, BaseMQTTMessage):
        except Exception as e:
            print("e", e)
            print("msg", msg)
            pass
        
        if hasattr(msg, 'decoded'):
            self.decoded = msg.decoded
        else:
            # decode payload into json object
            try: 
                # msg = self.msg.decode('utf-8')
                msg = {k: v.decode('utf-8') if isinstance(v, bytes) else v for k, v in self.msg.items()}
                # self.msg = json.loads(msg)
                self.decoded = True
            except Exception as e:
                self.msg = {
                    'flag': False,
                    'data': [],
                    'message': f'msg load fail: {e}'
                }

    def handle_msg(self, handler: Callable, **kwargs):
        handler(self, **kwargs)
    
if __name__ == '__main__':
    base_msg = {'topic': 'base_msg', 'payload': {'cls': 'base msg'}}
    demo_msg = {'topic': 'dev/dg3/s05/abc//sub/test_demo', 'payload': {'cls': 'dcfx msg'}}
    
    base_from_base = BaseMQTTMessage(base_msg)
    print(f'base_from_base.payload[cls]: {base_from_base.payload["cls"]}')
    
    base_from_demo = BaseMQTTMessage(demo_msg)
    print(f'base_from_demo.payload[cls]: {base_from_demo.payload["cls"]}')
    
    # super to child
    demo_from_base = DCFXMessage(base_from_demo)
    print(f'demo_from_base.payload[cls]: {demo_from_base.payload["cls"]}')
    print(f'demo_from_base.msg_name: {demo_from_base.msg_name}')
    
    demo_from_demo = DCFXMessage(demo_msg)
    print(f'demo_from_demo.payload[cls]: {demo_from_demo.payload["cls"]}')
    print(f'demo_from_demo.msg_name: {demo_from_demo.msg_name}')
    
    device_manager = {'device_dict': ['TEST FOR MSG HANDLER']}
    def test_handler(dcfx_msg: DCFXMessage, device_manager):
        print(f'get len(device_manager["device_dict"]): [{len(device_manager["device_dict"])}] at {dcfx_msg.now}')

    if demo_from_base.match_msg_topic('#'):
        # Arbitrary Keyword Arguments should specify variable name or put all variables in '**{}'
        demo_from_base.handle_msg(test_handler, device_manager=device_manager)
        demo_from_base.handle_msg(test_handler, **{'device_manager': device_manager})