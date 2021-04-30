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
        res = None

        try:
            if method == 'GET':
                res = requests.get(url=url, headers=headers)
            elif method == 'POST':
                res = requests.post(url=url, headers=headers, data=data)
            else:
                return None
        except Exception as e:
            raise RuntimeError('Failed to request')

        # print('[RESPONSE]\nStatus: {0}\nHeaders: {1}\nBody: {2}\nURL: {3}\nContent: {4}\n'.format(res.status_code, res.headers, res.text, res.url, res.content))

        return res
