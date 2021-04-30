import sys
import time
import requests
import json


class TransmitterReceiver:
    """ 요청, 응답 송수신기 """

    @staticmethod
    def get_response_for_request(host, path, headers, query, method, data=None):
        """ 요청 보내고 응답 받기 """
        # print('[REQUEST]\nHost: {0}\nPath: {1}\nHeaders: {2}\nQuery: {3}\nMethod: {4}\nData: {5}'.format(host, path, headers, query, method, data))
        url = host + path + query

        try:
            if method == 'GET':
                return requests.get(url=url, headers=headers)
            elif method == 'POST':
                return requests.post(url=url, headers=headers, data=data)
            else:
                return None
        except Exception as e:
            raise RuntimeError('Request failed')
