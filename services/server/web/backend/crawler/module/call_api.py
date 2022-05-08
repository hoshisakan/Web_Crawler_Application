import json
import requests
from .handle_exception import HandleException
from .log_generate import Loggings


logger = Loggings()

class APIRequest():
    def __init__(self, endpoint):
        self.__endpoint = endpoint

    def deleteRequestByPayload(self, data=[], header=''):
        response_data = {}
        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {header}'
            }
            response = requests.delete(url=self.__endpoint, headers=headers, data=json.dumps(data), verify=False)
            res_status_code = response.status_code
            res_json = response.json()
            response_data = {'status_code': res_status_code, 'data': res_json}
            logger.info(response_data)
        except Exception as e:
            logger.error(HandleException.show_exp_detail_message(e))
        return True if 'status_code' in response_data and response_data['status_code'] in [202, 204] else False

    def postRequest(self, data=[], header=''):
        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {header}'
            }
            response = requests.post(url=self.__endpoint, headers=headers, data=json.dumps(data), verify=False)
            res_status_code = response.status_code
            logger.warning(f'Post request response status code: {res_status_code}, response reason: {response.reason}')
        except Exception as e:
            logger.error(HandleException.show_exp_detail_message(e))
        return True if res_status_code == 201 else False

    def getRequest(self, header=''):
        response_data = {}
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {header}'
        }
        response = requests.get(url=self.__endpoint, headers=headers, verify=False)
        res_status_code = response.status_code
        res_json = response.json()
        response_data = {'status_code': res_status_code, 'data': res_json}
        return response_data if 'status_code' in response_data and response_data['status_code'] == 200 else None