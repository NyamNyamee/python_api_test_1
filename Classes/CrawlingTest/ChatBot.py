import time
import requests
import json
from urllib import parse

from Classes.Util.TransmitterReceiver import TransmitterReceiver


class ChatBotCrawler:
    """ 챗봇 크롤러  """

    def __init__(self, simsimi_api_key, simsimi_version):
        self.simsimi_api_key = simsimi_api_key
        self.simsimi_version = simsimi_version

    def chat_with_simsimi(self, chat_message, language_type):
        """ 심심이 챗봇 채팅 """
        # 한글 메시지 인코딩
        if language_type == 'ko':
            chat_message = parse.quote(chat_message)

        host = 'https://wsapi.simsimi.com'
        path = '/{0}/talk'.format(self.simsimi_version)
        headers = {'Content-Type': 'application/json;charset=utf-8', 'x-api-key': self.simsimi_api_key}
        query = ''
        method = 'POST'
        data = '{"utext": "' + chat_message + '", "lang": "' + language_type + '"}'

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)
        except Exception as e:
            raise RuntimeError('[심심이] 챗봇 응답 요청 실패: ' + str(e))

        # json형태의 텍스트를 딕셔너리로 파싱
        parsed_object = json.loads(res.text)

        response_status = parsed_object['status']
        response_text = parsed_object['atext']
        response_lang = parsed_object['lang']

        # 한글 메시지 디코딩
        if response_lang == 'ko':
            response_text = parse.unquote(response_text)

        # 결과출력
        if response_status != 200:
            raise RuntimeError('[심심이] 챗봇 응답 요청 실패')

        now_time = time.strftime('%Y-%m-%d %H:%M:%S')
        print('[{0}] 심심이: {1}'.format(now_time.split()[1], response_text))
        print()
