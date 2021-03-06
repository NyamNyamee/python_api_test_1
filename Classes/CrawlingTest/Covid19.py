import sys
import time
import requests
import json
from operator import itemgetter

from Classes.Util.TransmitterReceiver import TransmitterReceiver

class Covid19Crawler:
    """ 코로나19 관련 크롤러 """

    def __init__(self, data_gov_key):
        self.data_gov_key = data_gov_key

    def get_vaccine_center_info_by_address(self, covid19_search_address):
        """ 한국 Covid19 백신 api """
        host = 'https://api.odcloud.kr'
        path = '/api/15077586/v1/centers'
        headers = None
        query = '?serviceKey={0}&perPage=1000'.format(self.data_gov_key)
        method = 'GET'
        data = None

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)
        except Exception as e:
            raise RuntimeError("[공공데이터포털] 코로나19 센터 정보 요청 실패: " + str(e))

        # 응답의 바디를 json형태로 파싱
        parsed_object = json.loads(res.text)

        center_count = parsed_object['totalCount']
        list_data = parsed_object['data']
        ordered_list_data = sorted(list_data, key=itemgetter('address'))

        print('전국 센터 개수: {0}'.format(str(center_count)))
        print('센터번호    |    우편번호    |                센터명                |                시설명                |            주소')
        for index, component in enumerate(ordered_list_data):
            center_id = component['id']
            center_name = component['centerName']
            center_address = component['address']
            center_facility_name = component['facilityName']
            center_zip_code = component['zipCode']

            # 사용자가 검색한 주소가 아니면 출력하지 않음
            if covid19_search_address not in center_address:
                continue

            print('{0:11}{1:16}{2:30}{3:30}{4}'.format(str(center_id), center_zip_code, center_name, center_facility_name, center_address))
        print()

    def search_national_issue_by_nation_name(self, nation_name):
        """ 국가명으로 코로나 이슈 검색 """
        host = 'http://apis.data.go.kr'
        path = '/1262000/CountryCovid19SafetyServiceNew/getCountrySafetyNewsListNew'
        headers = None
        query = '?serviceKey={0}&numOfRows=100&pageNo=1&cond[country_nm::EQ]={1}'.format(self.data_gov_key, nation_name)
        method = 'GET'
        data = None

        # 응답
        try:
            res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query,
                                                               method=method, data=data)
        except Exception as e:
            raise RuntimeError("[공공데이터포털] 코로나19 국가별 이슈 요청 실패: " + str(e))

        # 응답의 바디를 json형태로 파싱
        parsed_object = json.loads(res.text)

        issue_count = parsed_object['currentCount']
        list_data = parsed_object['data']

        if not list_data:
            print('해당 국가의 이슈는 없습니다.')
            print()
            return

        print('작성일        |        국가        |        타이틀')
        print('검색 개수: {0}'.format(str(issue_count)))
        for index, component in enumerate(list_data):
            issue_written_date = component['wrt_dt']
            issue_nation_name = component['country_nm']
            issue_title = component['title']

            print('{0:14}{1:11}{2}'.format(issue_written_date, issue_nation_name, issue_title))
        print()
