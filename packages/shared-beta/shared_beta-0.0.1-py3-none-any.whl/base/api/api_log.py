from dataclasses import dataclass
from enum import Enum
from pymongo import MongoClient
from base.config import MongoDBSettings

@dataclass
class ResponseStatusCode(Enum):
    Success = 200 # 正常請求
    Bad_Request = 400 # 錯誤請求 / 缺少對應參數
    Unauthorized = 401 # 未通過身分認證 (例如: 使用無效之API Key)
    Forbidden = 403 # 無訪問權限
    Not_Found = 404 # 訪問對象不存在
    Request_Timeout = 408 # 回覆超時
    Rate_Limit_Exceeded = 429 # 頻繁請求禁止
    Internal_Server_Error = 500 # 伺服器錯誤

class APILog:
    '''
    2023-07-06 Eric: moved from mongo_api/app/model/base.py 
    initialize an API log and use log_to_db to insert a log into DB
    '''
    def __init__(self) -> None:
        self.receive_timestamp = None
        self.ip = None
        self.api = None
        self.url = None
        self.target = None
        self.method = None
        self.status_code = None
        self.response_timestamp = None
        self.response_size = None

    def log_to_db(self):
        err_msg = ''
        try:
            with MongoClient(
                host=MongoDBSettings.HOST, 
                port=MongoDBSettings.PORT, 
                username=MongoDBSettings.USERNAME, 
                password=MongoDBSettings.PASSWORD, 
                authSource=MongoDBSettings.AUTH_SOURCE) as client:

                db = client['edgeDatabase']
                db.apiLog.insert_one({
                    'IP': self.ip,
                    'API': self.api,
                    'URL': self.url,
                    'Target': self.target,
                    'Method': self.method,
                    'StatusCode': self.status_code,
                    'TimeStamp': self.receive_timestamp,
                    'ResponseTimestamp': self.response_timestamp,
                    'ResponseSize': self.response_size
                })
        except Exception as e:
            err_msg = str(e)

        return err_msg
    