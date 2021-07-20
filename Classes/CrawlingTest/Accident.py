import sys
import time
import requests
import json
from operator import itemgetter

from Classes.Util.TransmitterReceiver import TransmitterReceiver

class AccidentCrawler:
    """ 사고 관련 크롤러 """

    def __init__(self, data_gov_key):
        self.data_gov_key = data_gov_key

    def get_car_accident_info_by_year_and_location(self, search_year, search_sido, search_gugun):
        """ 연도별, 지역별 교통사고정보 조회 """
        host = 'http://apis.data.go.kr'
        path = '/B552061/AccidentDeath/getRestTrafficAccidentDeath'
        headers = None
        query = '?serviceKey={0}&type=json&searchYear={1}&siDo={2}&guGun={3}&pageNo=1&numOfRows=100'.format(self.data_gov_key, search_year, search_sido, search_gugun)
        method = 'GET'
        data = None

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)
        except Exception as e:
            raise RuntimeError("[공공데이터포털] 교통사고정보 요청 실패: " + str(e))

        # 응답의 바디를 json형태로 파싱
        parsed_object = json.loads(res.text)

        list_items = parsed_object['items']['item']

        if not list_items:
            print('검색 건수가 없습니다')
            print()
            return

        print('검색 건수: {0}'.format(str(len(list_items))))
        print('발생월일시    |    주야구분    |    발생요일    |    사망자수    |    부상자수    |    사고유형 대분류    |    사고유형 중분류    |    사고유형    |    법규위반내용    |    도로형태    |    가해차종    |    피해차종')
        for index, component in enumerate(list_items):
            accident_occurrence_date = component['occrrnc_dt']
            accident_day_night_code = component['dght_cd']
            accident_day_code = component['occrrnc_day_cd']
            accident_death_count = component['dth_dnv_cnt']
            accident_injury_count = component['injpsn_cnt']
            accident_type_classification_level_code = component['acc_ty_lclas_cd']  # 사고유형 대분류
            accident_type_multiple_classification_level_code = component['acc_ty_mlsfc_cd']  # 사고유형 중분류
            accident_type_code = component['acc_ty_cd']  # 사고유형
            accident_assailant_violation_law_code = component['aslt_vtr_cd']  # 법규위반
            accident_road_type_code = component['road_frm_cd']  # 도로형태
            accident_assailant_vehicle_code = component['wrngdo_isrty_vhcty_lclas_cd']  # 가해차종코드
            accident_victim_vehicle_code = component['dmge_isrty_vhcty_lclas_cd']  # 피해차종코드
            print('{0:13}{1:14}{2:15}{3:15}{4:16}{5:20}{6:18}{7:14}{8:16}{9:14}{10:12}{11}'.format(
                accident_occurrence_date,
                self.transfer_search_code_to_string(response_column=1, response_value=accident_day_night_code),
                self.transfer_search_code_to_string(response_column=2, response_value=accident_day_code),
                str(accident_death_count),
                str(accident_injury_count),
                self.transfer_search_code_to_string(response_column=3, response_value=accident_type_classification_level_code),
                self.transfer_search_code_to_string(response_column=4, response_value=accident_type_multiple_classification_level_code),
                self.transfer_search_code_to_string(response_column=5, response_value=accident_type_code),
                self.transfer_search_code_to_string(response_column=6, response_value=accident_assailant_violation_law_code.strip()),
                self.transfer_search_code_to_string(response_column=7, response_value=accident_road_type_code),
                self.transfer_search_code_to_string(response_column=8, response_value=accident_assailant_vehicle_code),
                self.transfer_search_code_to_string(response_column=8, response_value=accident_victim_vehicle_code)
            ))

        print()

    def transfer_search_string_to_code(self, response_column, response_value, sido_code=None):
        """ 검색유형과 검색어에 따라 알맞은 코드를 리턴 """
        # 시도
        if response_column == 1:
            if '서울' in response_value:
                return 1100
            elif '부산' in response_value:
                return 1200
            elif '대전' in response_value:
                return 2500
            elif '대구' in response_value:
                return 2200
            elif '광주' in response_value:
                return 2400
            elif '인천' in response_value:
                return 2300
            elif '울산' in response_value:
                return 2600
            elif '세종' in response_value:
                return 2700
            elif '경기' in response_value:
                return 1300
            elif '강원' in response_value:
                return 1400
            elif '충남' in response_value or '충청남도' in response_value:
                return 1600
            elif '충북' in response_value or '충청북도' in response_value:
                return 1500
            elif '전남' in response_value or '전라남도' in response_value:
                return 1800
            elif '전북' in response_value or '전라북도' in response_value:
                return 1700
            elif '경남' in response_value or '경상남도' in response_value:
                return 2000
            elif '경북' in response_value or '경상북도' in response_value:
                return 1900
            elif '제주' in response_value:
                return 2100
            else:
                raise RuntimeError('정확한 시도명을 입력해 주세요')

        # 시군구
        elif response_column == 2:
            # 서울
            if sido_code == 1100:
                if '강남' in response_value:
                    return 1116
                elif '강동' in response_value:
                    return 1117
                elif '강북' in response_value:
                    return 1124
                elif '강서' in response_value:
                    return 1111
                elif '관악' in response_value:
                    return 1115
                elif '광진' in response_value:
                    return 1123
                elif '구로' in response_value:
                    return 1112
                elif '금천' in response_value:
                    return 1125
                elif '노원' in response_value:
                    return 1122
                elif '도봉' in response_value:
                    return 1107
                elif '동대문' in response_value:
                    return 1105
                elif '동작' in response_value:
                    return 1114
                elif '마포' in response_value:
                    return 1110
                elif '서대문' in response_value:
                    return 1109
                elif '서초' in response_value:
                    return 1119
                elif '성동' in response_value:
                    return 1104
                elif '성북' in response_value:
                    return 1106
                elif '송파' in response_value:
                    return 1118
                elif '양천' in response_value:
                    return 1120
                elif '영등포' in response_value:
                    return 1113
                elif '용산' in response_value:
                    return 1103
                elif '은평' in response_value:
                    return 1108
                elif '종로' in response_value:
                    return 1101
                elif '중구' in response_value:
                    return 1102
                elif '중랑' in response_value:
                    return 1121
                else:
                    raise RuntimeError('정확한 시군구 명을 입력해 주세요')
            # 부산
            elif sido_code == 1200:
                if '강서' in response_value:
                    return 1212
                elif '금정' in response_value:
                    return 1211
                elif '기장' in response_value:
                    return 1216
                elif '남구' in response_value:
                    return 1207
                elif '동구' in response_value:
                    return 1203
                elif '동래구' in response_value:
                    return 1206
                elif '북구' in response_value:
                    return 1208
                elif '사상' in response_value:
                    return 1215
                elif '사하' in response_value:
                    return 1210
                elif '서구' in response_value:
                    return 1202
                elif '수영' in response_value:
                    return 1214
                elif '연제' in response_value:
                    return 1213
                elif '영도' in response_value:
                    return 1204
                elif '중구' in response_value:
                    return 1201
                elif '진구' in response_value:
                    return 1205
                elif '해운대' in response_value:
                    return 1209
                else:
                    raise RuntimeError('정확한 시군구 명을 입력해 주세요')

            # 대구
            elif sido_code == 2200:
                if '남구' in response_value:
                    return 2204
                elif '달서' in response_value:
                    return 2207
                elif '달성' in response_value:
                    return 2208
                elif '동구' in response_value:
                    return 2202
                elif '북구' in response_value:
                    return 2205
                elif '서구' in response_value:
                    return 2203
                elif '수성' in response_value:
                    return 2206
                elif '중구' in response_value:
                    return 2201
                else:
                    raise RuntimeError('정확한 시군구 명을 입력해 주세요')

            # 인천
            elif sido_code == 2300:
                if '강화' in response_value:
                    return 2309
                elif '계양' in response_value:
                    return 2308
                elif '미추홀' in response_value:
                    return 2303
                elif '남동' in response_value:
                    return 2305
                elif '동구' in response_value:
                    return 2302
                elif '부평' in response_value:
                    return 2304
                elif '서구' in response_value:
                    return 2306
                elif '연수' in response_value:
                    return 2307
                elif '옹진' in response_value:
                    return 2310
                elif '중구' in response_value:
                    return 2301
                else:
                    raise RuntimeError('정확한 시군구 명을 입력해 주세요')

            # 광주
            elif sido_code == 2400:
                if '광산' in response_value:
                    return 2404
                elif '남구' in response_value:
                    return 2405
                elif '동구' in response_value:
                    return 2401
                elif '북구' in response_value:
                    return 2403
                elif '서구' in response_value:
                    return 2402
                else:
                    raise RuntimeError('정확한 시군구 명을 입력해 주세요')

            # 대전
            elif sido_code == 2500:
                if '대덕' in response_value:
                    return 2505
                elif '동구' in response_value:
                    return 2501
                elif '서구' in response_value:
                    return 2503
                elif '유성' in response_value:
                    return 2504
                elif '중구' in response_value:
                    return 2502
                else:
                    raise RuntimeError('정확한 시군구 명을 입력해 주세요')

            # 울산
            elif sido_code == 2600:
                if '남구' in response_value:
                    return 2602
                elif '동구' in response_value:
                    return 2603
                elif '북구' in response_value:
                    return 2604
                elif '울주' in response_value:
                    return 2605
                elif '중구' in response_value:
                    return 2601
                else:
                    raise RuntimeError('정확한 시군구 명을 입력해 주세요')

            # 세종
            elif sido_code == 2700:
                if '세종' in response_value:
                    return 2701
                else:
                    raise RuntimeError('정확한 시군구 명을 입력해 주세요')

            # 경기
            elif sido_code == 1300:
                if '가평' in response_value:
                    return 1322
                elif '고양' in response_value:
                    return 1318
                elif '과천' in response_value:
                    return 1332
                elif '광명' in response_value:
                    return 1309
                elif '광주' in response_value:
                    return 1319
                elif '구리' in response_value:
                    return 1310
                elif '군포' in response_value:
                    return 1333
                elif '김포' in response_value:
                    return 1327
                elif '남양주' in response_value:
                    return 1334
                elif '동두천' in response_value:
                    return 1330
                elif '부천' in response_value:
                    return 1306
                elif '성남' in response_value:
                    return 1303
                elif '수원' in response_value:
                    return 1302
                elif '시흥' in response_value:
                    return 1316
                elif '안산' in response_value:
                    return 1307
                elif '안성' in response_value:
                    return 1326
                elif '안양' in response_value:
                    return 1305
                elif '양평' in response_value:
                    return 1323
                elif '여주' in response_value:
                    return 1313
                elif '연천' in response_value:
                    return 1320
                elif '오산' in response_value:
                    return 1335
                elif '용인' in response_value:
                    return 1325
                elif '의왕' in response_value:
                    return 1336
                elif '의정부' in response_value:
                    return 1304
                elif '이천' in response_value:
                    return 1324
                elif '파주' in response_value:
                    return 1317
                elif '평택' in response_value:
                    return 1308
                elif '포천' in response_value:
                    return 1321
                elif '하남' in response_value:
                    return 1337
                elif '화성' in response_value:
                    return 1315
                else:
                    raise RuntimeError('정확한 시군구 명을 입력해 주세요')

            # 강원
            elif sido_code == 1400:
                if '강릉' in response_value:
                    return 1404
                elif '고성' in response_value:
                    return 1422
                elif '동해' in response_value:
                    return 1403
                elif '삼척' in response_value:
                    return 1407
                elif '속초' in response_value:
                    return 1405
                elif '양구' in response_value:
                    return 1420
                elif '양양' in response_value:
                    return 1423
                elif '영월' in response_value:
                    return 1415
                elif '원주' in response_value:
                    return 1402
                elif '인제' in response_value:
                    return 1421
                elif '정선' in response_value:
                    return 1417
                elif '철원' in response_value:
                    return 1418
                elif '춘천' in response_value:
                    return 1401
                elif '태백' in response_value:
                    return 1406
                elif '평창' in response_value:
                    return 1416
                elif '홍천' in response_value:
                    return 1412
                elif '화천' in response_value:
                    return 1419
                elif '횡성' in response_value:
                    return 1413
                else:
                    raise RuntimeError('정확한 시군구 명을 입력해 주세요')

            # 충북
            elif sido_code == 1500:
                if '괴산' in response_value:
                    return 1516
                elif '단양' in response_value:
                    return 1520
                elif '보은' in response_value:
                    return 1512
                elif '영동' in response_value:
                    return 1514
                elif '옥천' in response_value:
                    return 1513
                elif '음성' in response_value:
                    return 1517
                elif '제천' in response_value:
                    return 1503
                elif '증평' in response_value:
                    return 1521
                elif '진천' in response_value:
                    return 1515
                elif '청원' in response_value:
                    return 1511
                elif '청주' in response_value:
                    return 1501
                elif '충주' in response_value:
                    return 1502
                else:
                    raise RuntimeError('정확한 시군구 명을 입력해 주세요')

            # 충남
            elif sido_code == 1600:
                if '계룡' in response_value:
                    return 1624
                elif '공주' in response_value:
                    return 1605
                elif '금산' in response_value:
                    return 1611
                elif '논산' in response_value:
                    return 1615
                elif '당진' in response_value:
                    return 1623
                elif '보령' in response_value:
                    return 1604
                elif '부여' in response_value:
                    return 1616
                elif '서산' in response_value:
                    return 1606
                elif '서천' in response_value:
                    return 1617
                elif '아산' in response_value:
                    return 1603
                elif '연기' in response_value:
                    return 1613
                elif '예산' in response_value:
                    return 1621
                elif '천안' in response_value:
                    return 1602
                elif '청양' in response_value:
                    return 1619
                elif '태안' in response_value:
                    return 1612
                elif '홍성' in response_value:
                    return 1620
                else:
                    raise RuntimeError('정확한 시군구 명을 입력해 주세요')

            # 전북
            elif sido_code == 1700:
                if '고창' in response_value:
                    return 1719
                elif '군산' in response_value:
                    return 1702
                elif '김제' in response_value:
                    return 1706
                elif '남원' in response_value:
                    return 1705
                elif '무주' in response_value:
                    return 1713
                elif '부안' in response_value:
                    return 1720
                elif '순창' in response_value:
                    return 1717
                elif '완주' in response_value:
                    return 1711
                elif '익산' in response_value:
                    return 1723
                elif '임실' in response_value:
                    return 1715
                elif '장수' in response_value:
                    return 1714
                elif '전주' in response_value:
                    return 1701
                elif '정읍' in response_value:
                    return 1704
                elif '진안' in response_value:
                    return 1712
                else:
                    raise RuntimeError('정확한 시군구 명을 입력해 주세요')

            # 전남
            elif sido_code == 1800:
                if '강진' in response_value:
                    return 1822
                elif '고흥' in response_value:
                    return 1818
                elif '곡성' in response_value:
                    return 1813
                elif '광양' in response_value:
                    return 1808
                elif '구례' in response_value:
                    return 1814
                elif '나주' in response_value:
                    return 1806
                elif '담양' in response_value:
                    return 1812
                elif '목포' in response_value:
                    return 1802
                elif '무안' in response_value:
                    return 1825
                elif '보성' in response_value:
                    return 1819
                elif '순천' in response_value:
                    return 1804
                elif '신안' in response_value:
                    return 1832
                elif '여수' in response_value:
                    return 1803
                elif '영광' in response_value:
                    return 1828
                elif '영암' in response_value:
                    return 1824
                elif '완도' in response_value:
                    return 1830
                elif '장성' in response_value:
                    return 1829
                elif '장흥' in response_value:
                    return 1821
                elif '진도' in response_value:
                    return 1831
                elif '함평' in response_value:
                    return 1827
                elif '해남' in response_value:
                    return 1823
                elif '화순' in response_value:
                    return 1820
                else:
                    raise RuntimeError('정확한 시군구 명을 입력해 주세요')

            # 경북
            elif sido_code == 1900:
                if '경산' in response_value:
                    return 1935
                elif '경주' in response_value:
                    return 1903
                elif '고령' in response_value:
                    return 1923
                elif '구미' in response_value:
                    return 1906
                elif '군위' in response_value:
                    return 1912
                elif '김천' in response_value:
                    return 1904
                elif '문경' in response_value:
                    return 1909
                elif '봉화' in response_value:
                    return 1932
                elif '상주' in response_value:
                    return 1910
                elif '성주' in response_value:
                    return 1924
                elif '안동' in response_value:
                    return 1905
                elif '영덕' in response_value:
                    return 1917
                elif '영양' in response_value:
                    return 1916
                elif '영주' in response_value:
                    return 1907
                elif '영천' in response_value:
                    return 1908
                elif '예천' in response_value:
                    return 1930
                elif '울릉' in response_value:
                    return 1934
                elif '울진' in response_value:
                    return 1933
                elif '의성' in response_value:
                    return 1913
                elif '청도' in response_value:
                    return 1922
                elif '청송' in response_value:
                    return 1915
                elif '칠곡' in response_value:
                    return 1925
                elif '포항' in response_value:
                    return 1902
                else:
                    raise RuntimeError('정확한 시군구 명을 입력해 주세요')

            # 경남
            elif sido_code == 2000:
                if '거제' in response_value:
                    return 2010
                elif '거창' in response_value:
                    return 2028
                elif '고성' in response_value:
                    return 2022
                elif '김해' in response_value:
                    return 2008
                elif '남해' in response_value:
                    return 2024
                elif '마산' in response_value:
                    return 2001
                elif '밀양' in response_value:
                    return 2009
                elif '사천' in response_value:
                    return 2023
                elif '산청' in response_value:
                    return 2026
                elif '양산' in response_value:
                    return 2016
                elif '의령' in response_value:
                    return 2012
                elif '진주' in response_value:
                    return 2003
                elif '진해' in response_value:
                    return 2005
                elif '창녕' in response_value:
                    return 2014
                elif '창원' in response_value:
                    return 2004
                elif '통영' in response_value:
                    return 2006
                elif '하동' in response_value:
                    return 2025
                elif '함안' in response_value:
                    return 2013
                elif '함양' in response_value:
                    return 2027
                elif '합천' in response_value:
                    return 2029
                else:
                    raise RuntimeError('정확한 시군구 명을 입력해 주세요')

            # 제주
            elif sido_code == 2100:
                if '서귀포' in response_value:
                    return 2102
                elif '제주' in response_value:
                    return 2101
                else:
                    raise RuntimeError('정확한 시군구 명을 입력해 주세요')

    def transfer_search_code_to_string(self, response_column, response_value):
        """ 검색유형과 검색코드 따라 알맞은 문자열을 리턴 """
        # 주야코드
        if response_column == 1:
            if response_value == '1':
                return '주간'
            elif response_value == '2':
                return '야간'
        # 요일코드
        elif response_column == 2:
            if response_value == '1':
                return '일'
            elif response_value == '2':
                return '월'
            elif response_value == '3':
                return '화'
            elif response_value == '4':
                return '수'
            elif response_value == '5':
                return '목'
            elif response_value == '6':
                return '금'
            elif response_value == '7':
                return '토'

        # 사고유형 대분류
        elif response_column == 3:
            if response_value == '01':
                return '차대사람'
            elif response_value == '02':
                return '차대차'
            elif response_value == '03':
                return '차량단독'
            elif response_value == '04':
                return '철길건널목'
            elif response_value == '99':
                return '기타'

        # 사고유형 중분류
        elif response_column == 4:
            if response_value == '11':
                return '횡단중'
            elif response_value == '12':
                return '차도통행중'
            elif response_value == '13':
                return '길가장자리통행중'
            elif response_value == '14':
                return '보도통행중'
            elif response_value == '15':
                return '기타'
            elif response_value == '21':
                return '정면충돌'
            elif response_value == '22':
                return '측면충돌'
            elif response_value == '23':
                return '추돌'
            elif response_value == '24':
                return '기타'
            elif response_value == '26':
                return '후진중충돌'
            elif response_value == '31':
                return '공작물충돌'
            elif response_value == '32':
                return '도로이탈'
            elif response_value == '33':
                return '주/정차차량충돌'
            elif response_value == '34':
                return '전도전복'
            elif response_value == '35':
                return '기타'
            elif response_value == '36':
                return '운전자부재'
            elif response_value == '38':
                return '전도'
            elif response_value == '39':
                return '전복'
            elif response_value == '41':
                return '철길건널목'
            elif response_value == 'Z2':
                return '차단기돌파'
            elif response_value == 'Z3':
                return '경보기무시'
            elif response_value == 'Z4':
                return '직전진행'
            elif response_value == 'Z5':
                return '기타'
            elif response_value == 'Z6':
                return '기타'

        # 사고유형
        elif response_column == 5:
            if response_value == '01':
                return '횡단중'
            elif response_value == '02':
                return '차도통행중'
            elif response_value == '03':
                return '길가장자리통행중'
            elif response_value == '04':
                return '보도통행중'
            elif response_value == '05':
                return '기타'
            elif response_value == '21':
                return '정면충돌'
            elif response_value == '22':
                return '측면충돌'
            elif response_value == '23':
                return '추돌'
            elif response_value == 'Z1':
                return '진행중추돌'
            elif response_value == 'Z2':
                return '주정차중충돌'
            elif response_value == '25':
                return '기타'
            elif response_value == '26':
                return '후진중충돌'
            elif response_value == '32':
                return '공작물충돌'
            elif response_value == '34':
                return '도로이탈추락'
            elif response_value == '35':
                return '도로이탈기타'
            elif response_value == '33':
                return '주/정차차량충돌'
            elif response_value == '31':
                return '전도전복'
            elif response_value == '37':
                return '기타'
            elif response_value == '36':
                return '운전자부재'
            elif response_value == '38':
                return '전도'
            elif response_value == '39':
                return '전복'
            elif response_value == '41':
                return '철길건널목'
            elif response_value == 'Z4':
                return '차단기돌파'
            elif response_value == 'Z5':
                return '경보기무시'
            elif response_value == 'Z6':
                return '직전진행'
            elif response_value == 'Z7':
                return '기타'
            elif response_value == 'Z8':
                return '기타'

        # 가해자법규위반
        elif response_column == 6:
            if response_value == '01':
                return '과속'
            elif response_value == '02':
                return '중앙성침범'
            elif response_value == '03':
                return '신호위반'
            elif response_value == '04':
                return '안전거리미확보'
            elif response_value == '05':
                return '안전운전의무불이행'
            elif response_value == '06':
                return '교차로통행방법위반'
            elif response_value == '07':
                return '보행자보호의무위반'
            elif response_value == '99':
                return '기타'

        # 도로형태
        elif response_column == 7:
            if response_value == '01':
                return '터널안'
            elif response_value == '02':
                return '교량위'
            elif response_value == '03':
                return '고가도로위'
            elif response_value == '04':
                return '지하차도(도로)내'
            elif response_value == '05':
                return '기타단일로'
            elif response_value == 'Z1':
                return '횡단보도상'
            elif response_value == 'Z2':
                return '횡단보도부근'
            elif response_value == '06':
                return '교차로내'
            elif response_value == '07':
                return '교차로횡단보도내'
            elif response_value == '08':
                return '교차로부근'
            elif response_value == '10':
                return '철길건널목'
            elif response_value == '98':
                return '기타'
            elif response_value == '99':
                return '불명'
            elif response_value == 'Z3':
                return '기타/불명'

        # 차종
        elif response_column == 8:
            if response_value == '01':
                return '승용차'
            elif response_value == '02':
                return '승합차'
            elif response_value == '03':
                return '화물차'
            elif response_value == '04':
                return '특수차'
            elif response_value == '05':
                return '이륜차'
            elif response_value == '06':
                return '사륜오토바이(ATV)'
            elif response_value == '07':
                return '원동기장치자전거'
            elif response_value == '08':
                return '자전거'
            elif response_value == '09':
                return '개인형이동수단(PM)'
            elif response_value == '10':
                return '건설기계'
            elif response_value == '11':
                return '농기계'
            elif response_value == '12':
                return '보행자'
            elif response_value == '98':
                return '기타'
            elif response_value == '99':
                return '불명'
            elif response_value == 'Z1':
                return '열차'
            elif response_value == 'ZL':
                return '기타'
