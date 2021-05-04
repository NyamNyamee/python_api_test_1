import sys
import time
import requests
import json
from operator import itemgetter

from Classes.Util.TransmitterReceiver import TransmitterReceiver


class KakaoCrawler:
    """ 카카오 오픈 API """

    def __init__(self, kakao_app_id, kakao_app_name, kakao_app_native_key, kakao_app_rest_key, kakao_app_js_key, kakao_app_admin_key, kakao_app_domian, kakao_app_redirect_uri):
        self.kakao_app_id = kakao_app_id
        self.kakao_app_name = kakao_app_name
        self.kakao_app_native_key = kakao_app_native_key
        self.kakao_app_rest_key = kakao_app_rest_key
        self.kakao_app_js_key = kakao_app_js_key
        self.kakao_app_admin_key = kakao_app_admin_key
        self.kakao_app_domian = kakao_app_domian
        self.kakao_app_redirect_uri = kakao_app_redirect_uri

    def get_new_kakao_access_code(self):
        """ 인가코드 요청 """
        host = 'https://kauth.kakao.com'
        path = '/oauth/authorize'
        headers = None
        query = '?response_type=code&client_id=' + self.kakao_app_rest_key + '&redirect_uri=https://github.com/NyamNyamee&response_type=code&state=inwoo&prompt=login'
        method = 'GET'
        data = None

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)
        except Exception as e:
            raise RuntimeError("[카카오] 인가코드 요청 실패: " + str(e))

        print(res.url)

    def get_new_kakao_token(self, kakao_access_code):
        """ 토큰 요청 """
        host = 'https://kauth.kakao.com'
        path = '/oauth/token'
        headers = {'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'}
        query = ''
        method = 'POST'
        data = {
            "grant_type": "authorization_code",
            "client_id": self.kakao_app_rest_key,
            "redirect_uri": "https://github.com/NyamNyamee",
            "code": kakao_access_code,
        }

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)
        except Exception as e:
            raise RuntimeError("[카카오] 토큰 요청 실패: " + str(e))

        # 응답의 바디를 json형태로 파싱
        parsed_object = json.loads(res.text)
        access_token = parsed_object['access_token']

        return access_token

    def get_kakao_user_info(self, kakao_token):
        """ 사용자 정보 요청 """
        host = 'https://kapi.kakao.com'
        path = '/v2/user/me'
        headers = {'Authorization': 'Bearer ' + kakao_token}
        query = ''
        # query = '?target_id_type=user_id&property_keys=["properties.nickname"]&target_id=1713183353'
        method = 'GET'
        data = None

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)
        except Exception as e:
            raise RuntimeError("[카카오] 사용자 정보 요청 실패: " + str(e))

        # 응답의 바디를 json형태로 파싱
        parsed_object = json.loads(res.text)

        try:
            kakao_inwoo_app_user_id = parsed_object['id']
            kakao_inwoo_connected_time = parsed_object['connected_at']
            kakao_inwoo_app_account_info = parsed_object['kakao_account']
            kakao_inwoo_app_account_profile = kakao_inwoo_app_account_info['profile']
            kakao_inwoo_app_account_profile_nickname = kakao_inwoo_app_account_profile['nickname']
            kakao_inwoo_app_account_profile_image_url = kakao_inwoo_app_account_profile['profile_image_url']
            kakao_inwoo_app_account_profile_email = kakao_inwoo_app_account_info['email']
            kakao_inwoo_app_account_profile_age_range = kakao_inwoo_app_account_info['age_range']
            kakao_inwoo_app_account_profile_birthday = kakao_inwoo_app_account_info['birthday']
            kakao_inwoo_app_account_profile_gender = kakao_inwoo_app_account_info['gender']

            print('회원번호: {0}\n연결된 시점: {1}\n닉네임: {2}\n프로필 이미지 링크: {3}\n이메일: {4}\n연령대: {5}\n생일: {6}\n성별: {7}'.format(
                kakao_inwoo_app_user_id, kakao_inwoo_connected_time,
                kakao_inwoo_app_account_profile_nickname,
                kakao_inwoo_app_account_profile_image_url,
                kakao_inwoo_app_account_profile_email,
                kakao_inwoo_app_account_profile_age_range,
                kakao_inwoo_app_account_profile_birthday,
                kakao_inwoo_app_account_profile_gender))
        except Exception as e:
            kakao_inwoo_app_error_message = parsed_object['msg']

            print(str(kakao_inwoo_app_error_message))

        print()

    def get_kakao_token_info(self, kakao_token):
        """ 토큰 정보 요청 """
        host = 'https://kapi.kakao.com'
        path = '/v1/user/access_token_info'
        headers = {'Authorization': 'Bearer ' + kakao_token}
        query = ''
        method = 'GET'
        data = None

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)
        except Exception as e:
            raise RuntimeError("[카카오] 사용자 토큰 정보 요청 실패: " + str(e))

        # 응답의 텍스트를 json형태로 파싱
        parsed_object = json.loads(res.text)

        kakao_inwoo_app_user_id = parsed_object['id']
        kakao_inwoo_connected_time = parsed_object['expires_in']
        kakao_inwoo_app_id = parsed_object['app_id']

        print('회원번호: {0}\n만료시간(초): {1}\nApp ID: {2}'.format(kakao_inwoo_app_user_id,
                                                            str(round(int(kakao_inwoo_connected_time) / 60)) + "분 " +
                                                            str(int(kakao_inwoo_connected_time) % 60) + "초",
                                                            kakao_inwoo_app_id))
        print()

    def kakao_send_message_myself(self, kakao_token, text_message):
        """ 나에게 문자 보내기 """
        host = 'https://kapi.kakao.com'
        path = '/v2/api/talk/memo/default/send'
        headers = {'Authorization': 'Bearer ' + kakao_token}
        query = ''
        method = 'POST'
        message_text_object = {
            "object_type": "text",
            "text": text_message,
            "link": {
                "web_url": "https://github.com/NyamNyamee",
                "mobile_web_url": "https://github.com/NyamNyamee"
            },
            "button_title": "Visit NyamNyamee"
        }
        message_feed_object = {
            "object_type": "feed",
            "content": {
                "title": "카카오 나에게 문자보내기 테스트",
                "image_url": "https://miro.medium.com/max/325/1*Je4yF-xdHEluVvmS0qw8JQ.png",
                "image_width": 10,
                "image_height": 10,
                "description": text_message,
                "link": {
                    "web_url": "https://github.com/NyamNyamee",
                    "mobile_web_url": "https://github.com/NyamNyamee"
                }
            },
            "social": {
                "like_count": 41,
                "comment_count": 36,
                "view_count": 260,
            },
            "button_title": "Visit NyamNyamee"
        }
        data = {"template_object": json.dumps(message_feed_object)}

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)
        except Exception as e:
            raise RuntimeError("[카카오] 나에게 문자 보내기 요청 실패: " + str(e))

        # 응답의 텍스트를 json형태로 파싱
        parsed_object = json.loads(res.text)

        if parsed_object['result_code'] is None or parsed_object['result_code'] != 0:
            print('메시지 전송 실패')

        print('[알림] 메시지 전송 성공')
        print()

