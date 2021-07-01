import sys
import time
import requests
import json
from operator import itemgetter

from Classes.Util.TransmitterReceiver import TransmitterReceiver

class GyeonggiInfoCrawler:
    """ 경기도 정보 관련 크롤러 """

    def __init__(self, data_gg_gov_key):
        self.data_gg_gov_key = data_gg_gov_key

    def get_cctv_installation_info(self, gyeonggi_search_sigun_name, gyeonggi_search_page_index=1):
        """ CCTV 설치 현황 api """
        host = 'https://openapi.gg.go.kr'
        path = '/CCTV'
        headers = None
        query = '?KEY={0}&Type=json&pIndex={1}&pSize=1000&SIGUN_NM={2}'.format(self.data_gg_gov_key, gyeonggi_search_page_index, gyeonggi_search_sigun_name)
        method = 'GET'
        data = None

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)
        except Exception as e:
            raise RuntimeError("[경기데이터드림] CCTV 설치 현황 요청 실패: " + str(e))

        # 응답의 바디를 json형태로 파싱
        parsed_object = json.loads(res.text)

        try:
            list_data = parsed_object['CCTV']
            list_head = list_data[0]['head']
            total_count = list_head[0]['list_total_count']
            list_row = list_data[1]['row']
        except Exception as e:
            raise RuntimeError('[경기데이터드림] CCTV 설치 현황 데이터를 정상적으로 불러오지 못했습니다: ' + str(e))

        # 총 개수가 1000개 초과일 때, 페이지를 늘려가며 조회하기 위한 총 개수의 맨 앞자리 숫자
        total_count_first_number = total_count // 1000
        print('맨 앞자리 숫자: ' + str(total_count_first_number))

        if gyeonggi_search_page_index == 1:
            print('CCTV 총 개수:{0}'.format(total_count))
            print('번호 |    설치년월    | 카메라대수 | 카메라화소 |    목적    |                                                  도로명주소                                                  |        관리기관(전화번호)')
        for index, component in enumerate(list_row):
            index_number = (index + 1) + (gyeonggi_search_page_index - 1) * 1000
            install_date = component['INSTL_YM'] if component['INSTL_YM'] is not None else '-'
            cctv_count = component['CAMERA_CNT'] if component['CAMERA_CNT'] is not None else '-'
            cctv_pixel = component['CAMERA_PIXEL_CNT'] if component['CAMERA_PIXEL_CNT'] is not None else '-'
            install_purpose = component['INSTL_PUPRS_DIV_NM'] if component['INSTL_PUPRS_DIV_NM'] is not None else '-'
            road_address = component['REFINE_ROADNM_ADDR'] if component['REFINE_ROADNM_ADDR'] is not None else '-'
            management_insttitution_name = component['MANAGE_INST_NM'] if component['MANAGE_INST_NM'] is not None else '-'
            management_insttitution_tel = component['MANAGE_INST_TELNO'] if component['MANAGE_INST_TELNO'] is not None else '-'

            print('{0:6}{1:15}{2:12}{3:10}{4:10}{5:80}{6}({7})'.format(str(index_number), install_date, str(cctv_count), str(cctv_pixel), install_purpose, road_address, management_insttitution_name, management_insttitution_tel))

        # 현재 페이지와 총개수의 맨 앞 숫자가 같다면 종료
        if gyeonggi_search_page_index == total_count_first_number + 1:
            print()
            return

        # 페이지를 1씩 늘려가며 나머지 데이터 조회
        gyeonggi_search_page_index += 1
        self.get_cctv_installation_info(gyeonggi_search_sigun_name=gyeonggi_search_sigun_name, gyeonggi_search_page_index=gyeonggi_search_page_index)


    def get_local_store_info(self, gyeonggi_search_sigun_name, gyeonggi_search_page_index=1):
        """ 지역화폐 가맹점 현황 api """
        host = 'https://openapi.gg.go.kr'
        path = '/RegionMnyFacltStus'
        headers = None
        query = '?KEY={0}&Type=json&pIndex={1}&pSize=1000&SIGUN_NM={2}'.format(self.data_gg_gov_key,
                                                                               gyeonggi_search_page_index,
                                                                               gyeonggi_search_sigun_name)
        method = 'GET'
        data = None

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query,
                                                               method=method, data=data)
        except Exception as e:
            raise RuntimeError("[경기데이터드림] 지역화폐 가맹점 현황 요청 실패: " + str(e))

        # 응답의 바디를 json형태로 파싱
        parsed_object = json.loads(res.text)

        try:
            list_data = parsed_object['RegionMnyFacltStus']
            list_head = list_data[0]['head']
            total_count = list_head[0]['list_total_count']
            list_row = list_data[1]['row']
        except Exception as e:
            raise RuntimeError('[경기데이터드림] 지역화폐 가맹점 현황 데이터를 정상적으로 불러오지 못했습니다: ' + str(e))

        # 총 개수가 1000개 초과일 때, 페이지를 늘려가며 조회하기 위한 총 개수의 맨 앞자리 숫자
        total_count_first_number = total_count // 1000

        if gyeonggi_search_page_index == 1:
            print('지역화폐 가맹점 총 개수:{0}'.format(total_count))
            print('번호 |        상호명        |        분류        |        도로명 주소')
        for index, component in enumerate(list_row):
            index_number = (index + 1) + (gyeonggi_search_page_index - 1) * 1000
            store_name = component['CMPNM_NM'] if component['CMPNM_NM'] is not None else '-'
            store_type = component['INDUTYPE_NM'] if component['INDUTYPE_NM'] is not None else '-'
            store_road_address = component['REFINE_ROADNM_ADDR'] if component['REFINE_ROADNM_ADDR'] is not None else '-'

            print('{0:6}{1:30}{2:20}{3}'.format(str(index_number), store_name, store_type, store_road_address))

        # 현재 페이지와 총개수의 맨 앞 숫자가 같다면 종료
        if gyeonggi_search_page_index == total_count_first_number + 1:
            print()
            return

        # 페이지를 1씩 늘려가며 나머지 데이터 조회
        gyeonggi_search_page_index += 1
        self.get_local_store_info(gyeonggi_search_sigun_name=gyeonggi_search_sigun_name,
                                  gyeonggi_search_page_index=gyeonggi_search_page_index)

    def get_free_wifi_info(self, gyeonggi_search_sigun_name, gyeonggi_search_page_index=1):
        """ 무료 WIFI 사용가능 장소 api """
        host = 'https://openapi.gg.go.kr'
        path = '/FreeChargeWiFi'
        headers = None
        query = '?KEY={0}&Type=json&pIndex={1}&pSize=1000&SIGUN_NM={2}'.format(self.data_gg_gov_key,
                                                                               gyeonggi_search_page_index,
                                                                               gyeonggi_search_sigun_name)
        method = 'GET'
        data = None

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query,
                                                               method=method, data=data)
        except Exception as e:
            raise RuntimeError("[경기데이터드림] 무료 WIFI 사용가능 장소 요청 실패: " + str(e))

        # 응답의 바디를 json형태로 파싱
        parsed_object = json.loads(res.text)

        try:
            list_data = parsed_object['FreeChargeWiFi']
            list_head = list_data[0]['head']
            total_count = list_head[0]['list_total_count']
            list_row = list_data[1]['row']
        except Exception as e:
            raise RuntimeError('[경기데이터드림] 무료 WIFI 사용가능 장소 데이터를 정상적으로 불러오지 못했습니다: ' + str(e))

        # 총 개수가 1000개 초과일 때, 페이지를 늘려가며 조회하기 위한 총 개수의 맨 앞자리 숫자
        total_count_first_number = total_count // 1000

        if gyeonggi_search_page_index == 1:
            print('무료 와이파이 사용가능 장소 총 개수:{0}'.format(total_count))
            print('번호 |  설치일자  |        와이파이명        |    제공업체    |        설치장소        |                                사용가능장소                                |                            도로명주소                            |                관리기관(전화번호)')
        for index, component in enumerate(list_row):
            index_number = (index + 1) + (gyeonggi_search_page_index - 1) * 1000
            wifi_install_date = component['INSTL_YM'] if component['INSTL_YM'] is not None else '-'
            wifi_ssid_name = component['WIFI_SSID_INFO'] if component['WIFI_SSID_INFO'] is not None else '-'
            wifi_supply_company_name = component['SERVC_SUPLYCMPY_NM'] if component['SERVC_SUPLYCMPY_NM'] is not None else '-'
            wifi_install_place = component['TMP01'] if component['TMP01'] is not None else '-'
            wifi_install_place_detail = component['INSTL_PLC_DETAIL_DTLS'] if component['INSTL_PLC_DETAIL_DTLS'] is not None else '-'
            wifi_road_address = component['REFINE_ROADNM_ADDR'] if component['REFINE_ROADNM_ADDR'] is not None else '-'
            wifi_install_management_institution_name = component['MANAGE_INST_NM'] if component['MANAGE_INST_NM'] is not None else '-'
            wifi_install_management_institution_tel = component['MANAGE_INST_TELNO'] if component['MANAGE_INST_TELNO'] is not None else '-'

            print('{0:6}{1:12}{2:24}{3:16}{4:24}{5:80}{6:50}{7}({8})'.format(str(index_number), wifi_install_date, wifi_ssid_name, wifi_supply_company_name, wifi_install_place, wifi_install_place_detail, wifi_road_address, wifi_install_management_institution_name, wifi_install_management_institution_tel))

        # 현재 페이지와 총개수의 맨 앞 숫자가 같다면 종료
        if gyeonggi_search_page_index == total_count_first_number + 1:
            print()
            return

        # 페이지를 1씩 늘려가며 나머지 데이터 조회
        gyeonggi_search_page_index += 1
        self.get_free_wifi_info(gyeonggi_search_sigun_name=gyeonggi_search_sigun_name,
                                gyeonggi_search_page_index=gyeonggi_search_page_index)

    def get_public_toilet_info(self, gyeonggi_search_sigun_name, gyeonggi_search_page_index=1):
        """ 공중화장실 현황 api """
        host = 'https://openapi.gg.go.kr'
        path = '/Publtolt'
        headers = None
        query = '?KEY={0}&Type=json&pIndex={1}&pSize=1000&SIGUN_NM={2}'.format(self.data_gg_gov_key,
                                                                               gyeonggi_search_page_index,
                                                                               gyeonggi_search_sigun_name)
        method = 'GET'
        data = None

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query,
                                                               method=method, data=data)
        except Exception as e:
            raise RuntimeError("[경기데이터드림] 공중화장실 현황 요청 실패: " + str(e))

        # 응답의 바디를 json형태로 파싱
        parsed_object = json.loads(res.text)

        try:
            list_data = parsed_object['Publtolt']
            list_head = list_data[0]['head']
            total_count = list_head[0]['list_total_count']
            list_row = list_data[1]['row']
        except Exception as e:
            raise RuntimeError('[경기데이터드림] 공중화장실 현황 데이터를 정상적으로 불러오지 못했습니다: ' + str(e))

        # 총 개수가 1000개 초과일 때, 페이지를 늘려가며 조회하기 위한 총 개수의 맨 앞자리 숫자
        total_count_first_number = total_count // 1000

        if gyeonggi_search_page_index == 1:
            print('공중화장실 총 개수:{0}'.format(total_count))
            print('번호 |  설치일자  |    구분    |  남녀공용  |      개방시간      |  남대  |  남소  |  여대  |        관리기관        |            화장실명            |    도로명주소')
        for index, component in enumerate(list_row):
            index_number = (index + 1) + (gyeonggi_search_page_index - 1) * 1000
            toilet_install_date = component['INSTL_YY'] if component['INSTL_YY'] is not None else '-'
            toilet_div_name = component['PUBLFACLT_DIV_NM'] if component['PUBLFACLT_DIV_NM'] is not None else '-'
            toilet_unisex_yn = component['MALE_FEMALE_TOILET_YN'] if component['MALE_FEMALE_TOILET_YN'] is not None else '-'
            toilet_open_time = component['OPEN_TM_INFO'] if component['OPEN_TM_INFO'] is not None else '-'
            toilet_male_big = component['MALE_WTRCLS_CNT'] if component['MALE_WTRCLS_CNT'] is not None else '-'
            toilet_male_small = component['MALE_UIL_CNT'] if component['MALE_UIL_CNT'] is not None else '-'
            toilet_female_big = component['FEMALE_WTRCLS_CNT'] if component['FEMALE_WTRCLS_CNT'] is not None else '-'
            toilet_management_institution = component['MANAGE_INST_NM'] if component['MANAGE_INST_NM'] is not None else '-'
            toilet_name = component['PBCTLT_PLC_NM'] if component['PBCTLT_PLC_NM'] is not None else '-'
            toilet_road_address = component['REFINE_ROADNM_ADDR'] if component['REFINE_ROADNM_ADDR'] is not None else '-'

            print('{0:6}{1:10}{2:10}{3:12}{4:18}{5:8}{6:8}{7:8}{8:20}{9:24}{10}'.format(str(index_number),
                                                                                       toilet_install_date,
                                                                                       toilet_div_name,
                                                                                       toilet_unisex_yn,
                                                                                       toilet_open_time,
                                                                                       str(toilet_male_big),
                                                                                       str(toilet_male_small),
                                                                                       str(toilet_female_big),
                                                                                       toilet_management_institution,
                                                                                       toilet_name,
                                                                                       toilet_road_address))

        # 현재 페이지와 총개수의 맨 앞 숫자가 같다면 종료
        if gyeonggi_search_page_index == total_count_first_number + 1:
            print()
            return

        # 페이지를 1씩 늘려가며 나머지 데이터 조회
        gyeonggi_search_page_index += 1
        self.get_free_wifi_info(gyeonggi_search_sigun_name=gyeonggi_search_sigun_name,
                                gyeonggi_search_page_index=gyeonggi_search_page_index)

    def get_electric_gas_station_info(self, gyeonggi_search_sigun_name, gyeonggi_search_page_index=1):
        """ 전기차 충전소 현황 api """
        host = 'https://openapi.gg.go.kr'
        path = '/Elctychrgstatn'
        headers = None
        query = '?KEY={0}&Type=json&pIndex={1}&pSize=1000&SIGUN_NM={2}'.format(self.data_gg_gov_key,
                                                                               gyeonggi_search_page_index,
                                                                               gyeonggi_search_sigun_name)
        method = 'GET'
        data = None

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query,
                                                               method=method, data=data)
        except Exception as e:
            raise RuntimeError("[경기데이터드림] 전기차 충전소 현황 요청 실패: " + str(e))

        # 응답의 바디를 json형태로 파싱
        parsed_object = json.loads(res.text)

        try:
            list_data = parsed_object['Elctychrgstatn']
            list_head = list_data[0]['head']
            total_count = list_head[0]['list_total_count']
            list_row = list_data[1]['row']
        except Exception as e:
            raise RuntimeError('[경기데이터드림] 전기차 충전소 현황 데이터를 정상적으로 불러오지 못했습니다: ' + str(e))

        # 총 개수가 1000개 초과일 때, 페이지를 늘려가며 조회하기 위한 총 개수의 맨 앞자리 숫자
        total_count_first_number = total_count // 1000

        if gyeonggi_search_page_index == 1:
            print('공중화장실 총 개수:{0}'.format(total_count))
            print('번호 |            충전소            |            충천기타입            |            운영기관            |            도로명주소')
        for index, component in enumerate(list_row):
            index_number = (index + 1) + (gyeonggi_search_page_index - 1) * 1000
            electric_gas_station_name = component['CHRGSTATN_NM'] if component['CHRGSTATN_NM'] is not None else '-'
            electric_charger_type = component['CHARGER_TYPE_NM'] if component['CHARGER_TYPE_NM'] is not None else '-'
            electric_operating_institution = component['OPERT_INST_NM'] if component['OPERT_INST_NM'] is not None else '-'
            electric_gas_station_road_address = component['REFINE_ROADNM_ADDR'] if component['REFINE_ROADNM_ADDR'] is not None else '-'

            print('{0:6}{1:26}{2:30}{3:28}{4}'.format(str(index_number),
                                                         electric_gas_station_name,
                                                         electric_charger_type,
                                                         electric_operating_institution,
                                                         electric_gas_station_road_address,
                                                         ))

        # 현재 페이지와 총개수의 맨 앞 숫자가 같다면 종료
        if gyeonggi_search_page_index == total_count_first_number + 1:
            print()
            return

        # 페이지를 1씩 늘려가며 나머지 데이터 조회
        gyeonggi_search_page_index += 1
        self.get_free_wifi_info(gyeonggi_search_sigun_name=gyeonggi_search_sigun_name,
                                gyeonggi_search_page_index=gyeonggi_search_page_index)
