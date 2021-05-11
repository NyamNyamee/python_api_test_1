import sys
import time
import requests
import json
from operator import itemgetter

from Classes.Util.TransmitterReceiver import TransmitterReceiver


class GameCrawler:
    """ 게임 관련 크롤러 """

    def __init__(self, steam_key, blizzard_client_name, blizzard_client_id, blizzard_client_secret,
                 blizzard_redirect_url, blizzard_region, blizzard_locale):
        self.steam_key = steam_key
        self.blizzard_client_name = blizzard_client_name
        self.blizzard_client_id = blizzard_client_id
        self.blizzard_client_secret = blizzard_client_secret
        self.blizzard_redirect_url = blizzard_redirect_url
        self.blizzard_region = blizzard_region
        self.blizzard_locale = blizzard_locale
        self.blizzard_access_token = None

    def search_steam_game_name_by_game_name(self, game_name):
        """ 게임이름으로 스팀게임 조회 """
        host = 'https://api.steampowered.com'
        path = '/ISteamApps/GetAppList/v1/'
        headers = None
        query = ''
        method = 'GET'
        data = None

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query,
                                                               method=method, data=data)
        except Exception as e:
            raise RuntimeError("[공공데이터포털] 지난 날씨정보 요청 실패: " + str(e))

        # 응답의 바디를 json형태로 파싱
        parsed_object = json.loads(res.text)

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

    # def get_new_blizzard_authorization_code(self):
    #     """ 블리자드 인가 코드 요청 """
    #     host = 'https://' + self.blizzard_region + '.battle.net'
    #     path = '/oauth/authorize'
    #     headers = None
    #     query = '?response_type=code&client_id={0}&redirect_uri={1}&state=inwoo'.format(self.blizzard_client_id, self.blizzard_redirect_url)
    #     method = 'GET'
    #     data = None
    #
    #     # 응답
    #     try:
    #         res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query,
    #                                                            method=method, data=data)
    #     except Exception as e:
    #         raise RuntimeError("[Blizzard] 인증코드 요청 실패: " + str(e))
    #
    #     print(res.url)

    def get_new_blizzard_access_token(self):
        """ 블리자드 토큰 요청 """
        host = 'https://' + self.blizzard_region + '.battle.net'
        path = '/oauth/token'
        headers = None
        query = ''
        method = 'POST'
        data = {
            "grant_type": "client_credentials",
            "client_id": self.blizzard_client_id,
            "client_secret": self.blizzard_client_secret
        }

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query,
                                                               method=method, data=data)

            # json형태의 문자열 바디를 딕셔너리로 파싱
            parsed_object = json.loads(res.text)
            blizzard_access_token = parsed_object['access_token']

            # 멤버변수에 토큰, 리프레쉬토큰 값 지정
            self.blizzard_access_token = blizzard_access_token

        except Exception as e:
            raise RuntimeError("[Blizzard] 토큰 요청 실패: " + str(e))

    # def get_blizzard_user_info(self):
    #     """ 블리자드 유저 정보 요청 """
    #     host = 'https://' + self.blizzard_region + '.battle.net'
    #     path = '/oauth/userinfo'
    #     headers = {'Authorization': 'Bearer ' + self.blizzard_access_token}
    #     query = ''
    #     method = 'GET'
    #     data = None
    #
    #     # 응답
    #     try:
    #         res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query,
    #                                                            method=method, data=data)
    #
    #         # json형태의 문자열 바디를 딕셔너리로 파싱
    #         parsed_object = json.loads(res.text)
    #
    #         print(parsed_object)
    #     except Exception as e:
    #         raise RuntimeError("[Blizzard] 유저 정보 요청 실패: " + str(e))

    def get_blizzard_diablo_3_profile(self, d3_battle_tag):
        """ 디아블로3 프로필 보기 """
        host = 'https://' + self.blizzard_region + '.api.blizzard.com'
        path = '/d3/profile/{0}/'.format(d3_battle_tag)
        headers = {'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8'}
        query = '?locale={0}&access_token={1}'.format(self.blizzard_locale, self.blizzard_access_token)
        method = 'GET'
        data = None

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query,
                                                               method=method, data=data)

            # json형태의 문자열 바디를 딕셔너리로 파싱
            parsed_object = json.loads(res.text)

            paragon_level = parsed_object['paragonLevel']
            guild_name = 'None' if parsed_object['guildName'] == '' else parsed_object['guildName']
            heroes = parsed_object['heroes']
            kills_monsters = str(parsed_object['kills']['monsters'])
            kills_elites = str(parsed_object['kills']['elites'])
            kills_hardcore_monsters = str(parsed_object['kills']['hardcoreMonsters'])

            print('정복자레벨: {0}\n길드명: {1}\n몬스터킬수 일반/엘리트/하드코어: {2}\n영웅:'.format(paragon_level, guild_name,
                                                                             kills_monsters + '/' + kills_elites + '/' + kills_hardcore_monsters))
            for index, component in enumerate(heroes):
                print('\t{0}. 이름:{1}\t클래스:{2}\t레벨:{3}'.format(str(index + 1), component['name'], component['class'], str(component['level'])))

            self.get_blizzard_diablo_3_hero_info(d3_battle_tag=d3_battle_tag, list_heroes=heroes)
            print()
        except Exception as e:
            raise RuntimeError("[Blizzard] Diablo3 프로필 요청 실패: " + str(e))

    def get_blizzard_diablo_3_hero_info(self, d3_battle_tag, list_heroes):
        """ 디아블로3 영웅 검색 """
        try:
            selected_diablo_3_hero = int(input('영웅 상세정보를 보려면 번호를 입력해 주세요. (0입력 시 메뉴로 이동)\n'))
            # 0 이하거나, 영화목록 개수보다 큰 수를 입력했을 때 리턴
            if selected_diablo_3_hero <= 0 or selected_diablo_3_hero > len(list_heroes):
                return
        except Exception as e:
            return

        host = 'https://' + self.blizzard_region + '.api.blizzard.com'
        path = '/d3/profile/{0}/hero/{1}'.format(d3_battle_tag, list_heroes[selected_diablo_3_hero - 1]['id'])
        headers = {'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8'}
        query = '?locale={0}&access_token={1}'.format(self.blizzard_locale, self.blizzard_access_token)
        method = 'GET'
        data = None

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query,
                                                               method=method, data=data)
        except Exception as e:
            raise RuntimeError("[Blizzard] Diablo3 영웅 정보 요청 실패: " + str(e))

        # 응답의 바디를 json형태로 파싱
        parsed_object = json.loads(res.text)

        list_active_skills = parsed_object['skills']['active']
        list_passive_skills = parsed_object['skills']['passive']

        dict_items = parsed_object['items']
        dict_items_head = dict_items['head']
        dict_items_neck = dict_items['neck']
        dict_items_torso = dict_items['torso']
        dict_items_shoulders = dict_items['shoulders']
        dict_items_legs = dict_items['legs']
        dict_items_waist = dict_items['waist']
        dict_items_hands = dict_items['hands']
        dict_items_bracers = dict_items['bracers']
        dict_items_feet = dict_items['feet']
        dict_items_left_finger = dict_items['leftFinger']
        dict_items_right_finger = dict_items['rightFinger']
        dict_items_main_hand = dict_items['mainHand']
        dict_items_off_hand = dict_items['offHand']

        dict_stats = parsed_object['stats']
        stat_life = dict_stats['life']
        stat_damage = dict_stats['damage']
        stat_attackSpeed = dict_stats['attackSpeed']
        stat_armor = dict_stats['armor']
        stat_strength = dict_stats['strength']
        stat_dexterity = dict_stats['dexterity']
        stat_vitality = dict_stats['vitality']
        stat_intelligence = dict_stats['intelligence']
        stat_physicalResist = dict_stats['physicalResist']
        stat_fireResist = dict_stats['fireResist']
        stat_coldResist = dict_stats['coldResist']
        stat_lightningResist = dict_stats['lightningResist']
        stat_poisonResist = dict_stats['poisonResist']
        stat_arcaneResist = dict_stats['arcaneResist']
        stat_critChance = dict_stats['critChance']
        stat_thorns = dict_stats['thorns']
        stat_lifeSteal = dict_stats['lifeSteal']
        stat_lifePerKill = dict_stats['lifePerKill']
        stat_lifeOnHit = dict_stats['lifeOnHit']

        print('스킬(패시브):')
        for index, component in enumerate(list_passive_skills):
            print('\t이름:{0:30}\t레벨:{1}\t아이콘:{2}'.format(component['skill']['name'], str(component['skill']['level']), 'http://media.blizzard.com/d3/icons/skills/64/' + component['skill']['icon'] + '.png'))
        print('스킬(액티브):')
        for index, component in enumerate(list_active_skills):
            print('\t이름:{0:30}\t레벨:{1}\t아이콘:{2}'.format(component['skill']['name'], str(component['skill']['level']),
                                                   'http://media.blizzard.com/d3/icons/skills/64/' + component['skill'][
                                                       'icon'] + '.png'))

        print('아이템:')
        print('\t머리     - 이름:{0:30}\t아이콘:{1}'.format(dict_items_head['name'], 'http://media.blizzard.com/d3/icons/items/large/' + dict_items_head['icon'] + '.png'))
        print('\t목       - 이름:{0:30}\t아이콘:{1}'.format(dict_items_neck['name'], 'http://media.blizzard.com/d3/icons/items/large/' + dict_items_neck['icon'] + '.png'))
        print('\t몸       - 이름:{0:30}\t아이콘:{1}'.format(dict_items_torso['name'], 'http://media.blizzard.com/d3/icons/items/large/' + dict_items_torso['icon'] + '.png'))
        print('\t어깨     - 이름:{0:30}\t아이콘:{1}'.format(dict_items_shoulders['name'], 'http://media.blizzard.com/d3/icons/items/large/' + dict_items_shoulders['icon'] + '.png'))
        print('\t다리     - 이름:{0:30}\t아이콘:{1}'.format(dict_items_legs['name'], 'http://media.blizzard.com/d3/icons/items/large/' + dict_items_legs['icon'] + '.png'))
        print('\t허리     - 이름:{0:30}\t아이콘:{1}'.format(dict_items_waist['name'], 'http://media.blizzard.com/d3/icons/items/large/' + dict_items_waist['icon'] + '.png'))
        print('\t손       - 이름:{0:30}\t아이콘:{1}'.format(dict_items_hands['name'], 'http://media.blizzard.com/d3/icons/items/large/' + dict_items_hands['icon'] + '.png'))
        print('\t팔목     - 이름:{0:30}\t아이콘:{1}'.format(dict_items_bracers['name'], 'http://media.blizzard.com/d3/icons/items/large/' + dict_items_bracers['icon'] + '.png'))
        print('\t발       - 이름:{0:30}\t아이콘:{1}'.format(dict_items_feet['name'], 'http://media.blizzard.com/d3/icons/items/large/' + dict_items_feet['icon'] + '.png'))
        print('\t왼손가락  - 이름:{0:30}\t아이콘:{1}'.format(dict_items_left_finger['name'], 'http://media.blizzard.com/d3/icons/items/large/' + dict_items_left_finger['icon'] + '.png'))
        print('\t오른손가락 - 이름:{0:30}\t아이콘:{1}'.format(dict_items_right_finger['name'], 'http://media.blizzard.com/d3/icons/items/large/' + dict_items_right_finger['icon'] + '.png'))
        print('\t주무기    - 이름:{0:30}\t아이콘:{1}'.format(dict_items_main_hand['name'], 'http://media.blizzard.com/d3/icons/items/large/' + dict_items_main_hand['icon'] + '.png'))
        print('\t보조무기  - 이름:{0:30}\t아이콘:{1}'.format(dict_items_off_hand['name'], 'http://media.blizzard.com/d3/icons/items/large/' + dict_items_off_hand['icon'] + '.png'))

        print('스탯:')
        print('\tlife: {0}'.format(stat_life))
        print('\tdamage: {0}'.format(stat_damage))
        print('\tattackSpeed: {0}'.format(stat_attackSpeed))
        print('\tarmor: {0}'.format(stat_armor))
        print('\tstrength: {0}'.format(stat_strength))
        print('\tdexterity: {0}'.format(stat_dexterity))
        print('\tvitality: {0}'.format(stat_vitality))
        print('\tintelligence: {0}'.format(stat_intelligence))
        print('\tphysicalResist: {0}'.format(stat_physicalResist))
        print('\tfireResist: {0}'.format(stat_fireResist))
        print('\tcoldResist: {0}'.format(stat_coldResist))
        print('\tlightningResist: {0}'.format(stat_lightningResist))
        print('\tpoisonResist: {0}'.format(stat_poisonResist))
        print('\tarcaneResist: {0}'.format(stat_arcaneResist))
        print('\tcritChance: {0}'.format(stat_critChance))
        print('\tthorns: {0}'.format(stat_thorns))
        print('\tlifeSteal: {0}'.format(stat_lifeSteal))
        print('\tlifePerKill: {0}'.format(stat_lifePerKill))
        print('\tlifeOnHit: {0}'.format(stat_lifeOnHit))

