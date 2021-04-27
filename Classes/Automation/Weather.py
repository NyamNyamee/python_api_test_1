import sys
import time
import requests
import json


class WeatherCrawler:
    """ 날씨정보 크롤러 """

    def __init__(self, data_gov_key):
        self.data_gov_key = data_gov_key

    def get_ex_weather_info(self, start_date, end_date, weather_location):
        """ 지난 날씨정보 검색 """
        # url
        url = 'http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList?serviceKey={0}&pageNo=1&numOfRows=100&dataType=JSON&dataCd=ASOS&dateCd=HR&startDt={1}&startHh=01&endDt={2}&endHh=23&stnIds={3}'.format(
            self.data_gov_key, start_date, end_date, weather_location)

        try:
            # 요청보내고 응답 저장
            res = requests.get(url)
            # 응답의 텍스트
            res_text = res.text
            # 응답의 텍스트를 json형태로 파싱
            parsed_object = json.loads(res_text)
            # 위 두줄을 아래와 같이 사용해도 됨
            # parsed_object = res.json()
        except Exception as e:
            raise RuntimeError('공공데이터포털로부터 정보를 가져오는 데에 실패했습니다.')

        # 날씨 리스트만 가져옴
        list_items = parsed_object['response']['body']['items']['item']

        print('번호    |        시각        |        관측지점         |     온도     |     습도     |     풍속    |    강수량')

        for index, component in enumerate(list_items):
            ex_weather_index = component['rnum']
            ex_weather_date = component['tm']
            ex_weather_station_name = component['stnNm']
            ex_weather_temperature = component['ta']
            ex_weather_humidity = component['hm']
            ex_weather_wind_speed = component['ws']
            ex_weather_rainfall = '0' if not component['rn'] else component['rn']

            print('{0:8}{1:20}{2:24}{3:14}{4:14}{5:13}{6}'.format(ex_weather_index, ex_weather_date,
                                                                  ex_weather_station_name, ex_weather_temperature,
                                                                  ex_weather_humidity, ex_weather_wind_speed,
                                                                  ex_weather_rainfall))
        print()
