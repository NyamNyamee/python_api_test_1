import sys
import time
import requests
import json

from operator import itemgetter

from Classes.Util.TransmitterReceiver import TransmitterReceiver

class KakaoCrawler:
    """ 카카오 오픈 API """

    def __init__(self, kakao_inwoo_admin_key, kakao_inwoo_token):
        self.kakao_inwoo_admin_key = kakao_inwoo_admin_key
        self.kakao_inwoo_token = kakao_inwoo_token

    def get_kakao_user_info(self):
        """ 사용자 정보 요청 """
        host = 'https://kapi.kakao.com'
        path = '/v2/user/me'
        headers = {'Authorization': 'Bearer ' + self.kakao_inwoo_token}
        query = ''
        # query = '?target_id_type=user_id&property_keys=["properties.nickname"]&target_id=1713183353'
        method = 'GET'
        data = None

        # 응답
        res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)
        # print('[RESPONSE]\nStatus: {0}\nHeaders: {1}\nBody: {2}\nURL: {3}\nContent: {4}'.format(res.status_code, res.headers, res.text, res.url, res.content))
        # 응답의 텍스트를 json형태로 파싱
        parsed_object = json.loads(res.text)

        print(parsed_object)
        print()

    def get_kakao_token_info(self):
        """ 사용자 토큰 정보 요청 """
        host = 'https://kapi.kakao.com'
        path = '/v1/user/access_token_info'
        headers = {'Authorization': 'Bearer ' + self.kakao_inwoo_token}
        query = ''
        method = 'GET'
        data = None

        # 응답
        res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)
        # print('[RESPONSE]\nStatus: {0}\nHeaders: {1}\nBody: {2}\nURL: {3}\nContent: {4}'.format(res.status_code, res.headers, res.text, res.url, res.content))
        # 응답의 텍스트를 json형태로 파싱
        parsed_object = json.loads(res.text)

        print(parsed_object)
        print()

    def kakao_send_message_myself(self, message_text):
        """ 나에게 문자 보내기 """
        host = 'https://kapi.kakao.com'
        path = '/v2/api/talk/memo/default/send'
        headers = {'Authorization': 'Bearer ' + self.kakao_inwoo_token}
        query = ''
        method = 'POST'
        message_object = {
            "object_type": "text",
            "text": message_text,
            "link": {
                "web_url": "https://github.com/NyamNyamee",
                "mobile_web_url": "https://github.com/NyamNyamee"
            },
            "button_title": "Visit NyamNyamee"
        }
        data = {"template_object": json.dumps(message_object)}

        # 응답
        res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)
        # print('[RESPONSE]\nStatus: {0}\nHeaders: {1}\nBody: {2}\nURL: {3}\nContent: {4}'.format(res.status_code, res.headers, res.text, res.url, res.content))
        # 응답의 텍스트를 json형태로 파싱
        parsed_object = json.loads(res.text)

        if parsed_object['result_code'] is None or parsed_object['result_code'] != 0:
            print('메시지 전송 실패')

        print('[알림] 메시지 전송 성공')
        print()
