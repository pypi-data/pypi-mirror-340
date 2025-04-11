import sys
from datetime import datetime
from base.api.api_log import APILog, ResponseStatusCode
from flask import Request

class BaseAPI:
    '''
    a basic api class can be instantiated or inherited to implement 3 features:
    1. API log (to DB)
    2. simple required param validation
    3. unified response data format

    * params:
    request: the http request context object
    request_params: the api request param dict
    required_params: the required param names to be validated
    
    * response data format
    flag: True as default, if it sets to False then message must describes error reason.
    data: empty list as default, the bool reflect if data is a complex object (even include)
    message: empty string as default, describe an error message if flag is False.
    
    '''
    def __init__(self, request: Request, request_params: dict=dict(), required_params: set=set(), with_log: bool=False) -> None:
        self.request_params = request_params
        self.required_params = required_params

        # init log
        self.log = APILog()
        self.log.receive_timestamp = datetime.utcnow()
        self.log.ip = request.access_route
        self.log.api = request.path
        self.log.url = request.url
        self.log.method = request.method
        self.log.status_code = ResponseStatusCode.Success.value
        
        self.with_log = with_log

        self.response_code = 0
        self.response_data = []
        self.response_message = 'OK'


    def set_response_message(self, message: str, overwrite: bool = False):
        try:
            if overwrite == True:
                self.response_message = str(message)
            else:
                self.response_message = f"{self.response_message} {message}"
            return True
        except Exception as e:
            print(f"Set API message failed with error: {e}")
            return False


    def get_result(self):
        '''
        log api request to db and return a response message
        '''

        # log to db
        self.log.response_timestamp = datetime.now()
        self.log.response_size = sys.getsizeof(self.response_data)
        if self.with_log is True:
            log_msg = self.log.log_to_db()
            if log_msg:
                self.response_code = 1
                self.response_message = f'log error: {log_msg} \n {self.response_message}'

        return {
            'code': self.response_code,
            'data': self.response_data,
            'msg': self.response_message
        }

    def check_params(self):
        '''
        evaluate whether all required params are included in the request,
        if no the response content will be updated with missing variables;
        users need to check the response and write crresponding control codes
        '''

        # todo consider flask_request_parser
        # return request_parser.parse_args()

        missing_params = [item for item in self.required_params 
                          if item not in self.request_params]
        
        if len(missing_params) != 0:
            self.response_code = 1
            self.response_message = f'missing params: {missing_params}'
            
            # bad request
            self.log.status_code = ResponseStatusCode.Bad_Request.value
