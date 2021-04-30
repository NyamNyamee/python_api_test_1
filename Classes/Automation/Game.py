import sys
import time
import requests
import json

from operator import itemgetter


class GameCrawler:
    """ 게임 관련 크롤러 """

    def __init__(self, steam_key):
        self.steam_key = steam_key

    def search_steam_game_name_by_game_name(self, game_name):
        """ 게임이름으로 게임이름 조회 """
        # url
        url = 'https://api.steampowered.com/ISteamApps/GetAppList/v1/'

        try:
            # 요청보내고 응답 저장
            res = requests.get(url)
            # 응답의 텍스트
            res_text = res.text
            # 응답의 텍스트를 json형태로 파싱
            parsed_object = json.loads(res_text)
            # 위 두줄과 아래 한줄은 동일
            # parsed_object = res.json()
        except Exception as e:
            raise RuntimeError('Steam으로부터 정보를 가져오는 데에 실패했습니다.')

        list_apps = parsed_object['applist']['apps']['app']

        print('스팀게임 총 개수: {0}'.format(str(len(list_apps))))
        print('고유번호    |    게임명')
        for index, component in enumerate(list_apps):
            steam_game_id = component['appid']
            steam_game_name = component['name']

            # 사용자가 검색한 주소가 아니면 출력하지 않음
            if game_name not in steam_game_name.lower():
                continue

            print('{0:11}{1}'.format(str(steam_game_id), steam_game_name))
        print()


