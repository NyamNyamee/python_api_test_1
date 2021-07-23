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
        self.kakao_access_token = None
        self.kakao_access_refresh_token = None

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

    def get_new_kakao_access_token(self, kakao_access_code):
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

            # json형태의 문자열 바디를 딕셔너리로 파싱
            parsed_object = json.loads(res.text)
            access_token = parsed_object['access_token']
            access_refresh_token = parsed_object['refresh_token']

            # 멤버변수에 토큰, 리프레쉬토큰 값 지정
            self.kakao_access_token = access_token
            self.kakao_access_refresh_token = access_refresh_token
        except Exception as e:
            raise RuntimeError("[카카오] 토큰 요청 실패: " + str(e))

    def get_kakao_token_info(self):
        """ 토큰 정보 요청 """
        host = 'https://kapi.kakao.com'
        path = '/v1/user/access_token_info'
        headers = {'Authorization': 'Bearer ' + self.kakao_access_token}
        query = ''
        method = 'GET'
        data = None

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)

            # json형태의 문자열 바디를 딕셔너리로 파싱
            parsed_object = json.loads(res.text)

            kakao_inwoo_app_user_id = parsed_object['id']
            kakao_inwoo_connected_time = parsed_object['expires_in']
            kakao_inwoo_app_id = parsed_object['app_id']

            print('회원번호: {0}\n만료시간: {1}\nApp ID: {2}'.format(kakao_inwoo_app_user_id,
                                                             str(round(
                                                                 int(kakao_inwoo_connected_time) / 60)) + "분 " +
                                                             str(int(kakao_inwoo_connected_time) % 60) + "초",
                                                             kakao_inwoo_app_id))

            print()
        except Exception as e:
            raise RuntimeError("[카카오] 사용자 토큰 정보 요청 실패: " + str(e))

    def refresh_kakao_access_token(self):
        """ 토큰 갱신 """
        host = 'https://kauth.kakao.com'
        path = '/oauth/token'
        headers = {'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'}
        query = ''
        method = 'POST'
        data = {
            "grant_type": "refresh_token",
            "client_id": self.kakao_app_rest_key,
            "refresh_token": self.kakao_access_refresh_token
        }

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)

            # json형태의 문자열 바디를 딕셔너리로 파싱
            parsed_object = json.loads(res.text)
            access_token = parsed_object['access_token']

            # 멤버변수에 토큰 값 지정
            self.kakao_access_token = access_token
        except Exception as e:
            raise RuntimeError("[카카오] 토큰 갱신 실패: " + str(e))

        print('[알림] 토큰 갱신 성공')
        print()

    def get_kakao_user_list(self):
        """ 사용자 목록 요청 """
        host = 'https://kapi.kakao.com'
        path = '/v1/user/ids'
        headers = {'Authorization': 'KakaoAK ' + self.kakao_app_admin_key, 'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'}
        query = '?limit=100'
        method = 'GET'
        data = None

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)

            # json형태의 문자열 바디를 딕셔너리로 파싱
            parsed_object = json.loads(res.text)

            kakao_inwoo_app_total_count = parsed_object['total_count']
            kakao_inwoo_app_user_list = parsed_object['elements']

            # 딕셔너리 크기가 4이면, 이전페이지와 다음페이지가 존재한다는 의미임
            if len(parsed_object) == 4:
                kakao_inwoo_app_user_list_after_url = parsed_object['after_url']
                kakao_inwoo_app_user_list_before_url = parsed_object['before_url']
                print('{0} 앱 사용자: {1}명\n다음 페이지: {2}\n이전 페이지: {3}'.format(self.kakao_app_name, str(kakao_inwoo_app_total_count), kakao_inwoo_app_user_list_after_url, kakao_inwoo_app_user_list_before_url))
            else:
                print('{0} 앱 사용자: {1}명'.format(self.kakao_app_name, str(kakao_inwoo_app_total_count)))

            print('번호    |    회원번호')
            for index, component in enumerate(kakao_inwoo_app_user_list):
                print('{0:8}{1}'.format(str(index + 1), str(component)))

            # 사용자 정보 요청
            self.get_kakao_user_info(kakao_app_user_list=kakao_inwoo_app_user_list)
        except Exception as e:
            raise RuntimeError("[카카오] 사용자 목록 요청 실패: " + str(e))

    def get_kakao_user_info(self, kakao_app_user_list):
        """ 회원번호로 사용자 정보 요청 """
        try:
            # 사용자가 번호 선택
            selected_user_property_id = int(input('사용자 정보를 보시려면 번호를 입력해주세요. (0입력 시 메뉴로 이동)\n'))
            # 0 이하거나, 영화목록 개수보다 큰 수를 입력했을 때 리턴
            if selected_user_property_id <= 0 or selected_user_property_id > len(kakao_app_user_list):
                print()
                return
        except Exception as e:
            print()
            return

        host = 'https://kapi.kakao.com'
        path = '/v2/user/me'
        headers = {'Authorization': 'KakaoAK ' + self.kakao_app_admin_key, 'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'}
        query = ''
        # query = '?target_id_type=user_id&property_keys=["properties.nickname"]&target_id=1713183353'
        method = 'POST'
        data = {
            "target_id_type": "user_id",
            "target_id": str(kakao_app_user_list[selected_user_property_id - 1])
        }

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)

            # json형태의 문자열 바디를 딕셔너리로 파싱
            parsed_object = json.loads(res.text)

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
                kakao_inwoo_app_user_id,
                kakao_inwoo_connected_time,
                kakao_inwoo_app_account_profile_nickname,
                kakao_inwoo_app_account_profile_image_url,
                kakao_inwoo_app_account_profile_email,
                kakao_inwoo_app_account_profile_age_range,
                kakao_inwoo_app_account_profile_birthday,
                kakao_inwoo_app_account_profile_gender))

            print()
        except Exception as e:
            kakao_inwoo_app_error_message = parsed_object['msg']
            raise RuntimeError("[카카오] 사용자 정보 요청 실패: " + str(kakao_inwoo_app_error_message))

    def kakao_send_message_myself(self, text_message):
        """ 나에게 문자 보내기 """
        host = 'https://kapi.kakao.com'
        path = '/v2/api/talk/memo/default/send'
        headers = {'Authorization': 'Bearer ' + self.kakao_access_token}
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
            "button_title": "Visit NyamNyamee.Github"
        }
        # dict타입을 json형태의 문자열로 인코딩
        data = {"template_object": json.dumps(message_feed_object)}

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)

            # json형태의 문자열 바디를 딕셔너리로 파싱
            parsed_object = json.loads(res.text)

            if parsed_object['result_code'] is None or parsed_object['result_code'] != 0:
                print('메시지 전송 실패')

            print('[알림] 메시지 전송 성공')
            print()
        except Exception as e:
            raise RuntimeError("[카카오] 나에게 문자 보내기 요청 실패: " + str(e))

    def kakao_translate(self, language_num_to_translate, language_num_to_translated, text_to_translate):
        """ 언어 번역 """
        language_num_to_translate = self. transfer_language_num_to_code(language_num_to_translate)
        language_num_to_translated = self.transfer_language_num_to_code(language_num_to_translated)

        host = 'https://dapi.kakao.com'
        path = '/v2/translation/translate'
        headers = {'Authorization': 'KakaoAK ' + self.kakao_app_rest_key, 'Content-type':'application/x-www-form-urlencoded'}
        query = ''
        method = 'POST'
        data = {
            "src_lang": language_num_to_translate,
            "target_lang": language_num_to_translated,
            "query": text_to_translate
        }

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)

            # json형태의 문자열 바디를 딕셔너리로 파싱
            parsed_object = json.loads(res.text)

            kakao_inwoo_app_traslated_text = parsed_object['translated_text']

            print('번역 결과:\n{0}'.format(kakao_inwoo_app_traslated_text))

            print()
        except Exception as e:
            raise RuntimeError("[카카오] 문장 번역 실패: " + str(e))

    def transfer_language_num_to_code(self, language_num):
        if language_num == 1:
            return 'kr'
        elif language_num == 2:
            return 'en'
        elif language_num == 3:
            return 'jp'
        elif language_num == 4:
            return 'cn'
        elif language_num == 5:
            return 'vi'
        elif language_num == 6:
            return 'id'
        elif language_num == 7:
            return 'ar'
        elif language_num == 8:
            return 'bn'
        elif language_num == 9:
            return 'de'
        elif language_num == 10:
            return 'es'
        elif language_num == 11:
            return 'fr'
        elif language_num == 12:
            return 'hi'
        elif language_num == 13:
            return 'it'
        elif language_num == 14:
            return 'ms'
        elif language_num == 15:
            return 'nl'
        elif language_num == 16:
            return 'pt'
        elif language_num == 17:
            return 'ru'
        elif language_num == 18:
            return 'th'
        elif language_num == 19:
            return 'tr'