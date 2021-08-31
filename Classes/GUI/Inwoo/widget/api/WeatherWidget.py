import sys
import time
import datetime
import json
import jproperties
import urllib.request

from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Classes.Util.Logger import logger

from Classes.Util.UnicodeUtil import UnicodeUtil
from Classes.Util.TransmitterReceiver import TransmitterReceiver


class WeatherWidget(QWidget):
    """ inwoo app weather widget """

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """ 생성자 """
        try:
            # .properties 파일 리더
            self.property_reader = jproperties.Properties()
            
            # 프로퍼티 파일 오픈
            # with open('../resources/auth.properties', 'rb') as auth_properties:
            with open('../resources/auth/auth.properties', 'rb') as auth_properties:
                self.property_reader.load(auth_properties)

            # 공공데이터포털 키
            self.data_gov_key = self.property_reader.get('DATA_GOV_KEY').data

            # 오늘날짜
            self.date_today = QDate().currentDate()

            # 폰트
            self.font_header = QFont()  # 헤더용 폰트 객체 생성
            self.font_header.setBold(True)  # 굵게
            self.font_header.setPointSize(8)  # 글자 포인트

            self.font_content = QFont()  # 내용물 폰트 객체 생성
            self.font_content.setPointSize(8)  # 글자 포인트

            # 날씨 수직 레이아웃 생성
            self.v_layout_weather = QVBoxLayout()
        except Exception as e:
            print('{init_ui} - ' + str(e))

    def get_progress_bar(self):
        """ 로딩바 설정 """
        try:
            # 생성
            progress_bar = QProgressBar(self)
            progress_bar.resize(200, 20)
            # progress_bar.setRange(0, 0)
            # 위치 설정
            qr = self.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            progress_bar.move(qr.center())
            # 숨김
            progress_bar.setVisible(False)

            return progress_bar
        except Exception as e:
            print('{get_progress_bar} - ' + str(e))

    def date_picker_handler(self):
        """ 날짜 변경 시 이벤트 핸들러 """
        try:
            # 각 날짜 값 저장
            selected_date_picker_01 = self.date_picker_01.date()
            selected_date_picker_02 = self.date_picker_02.date()

            self.date_picker_01.setMaximumDate(selected_date_picker_02)  # 시작 대출일 최대치를 끝 대출일 선택값으로
            self.date_picker_02.setMinimumDate(selected_date_picker_01)  # 끝 대출일 최소치를 시작 대출일 선택값으로
        except Exception as e:
            print('{date_picker_handler} - ' + str(e))

    def set_tabs_weather(self):
        """ 날씨 메뉴 탭 생성 """
        try:
            # 메인 위젯의 레이아웃을 날씨 수직 레이아웃으로 지정
            self.setLayout(self.v_layout_weather)

            # weather_tabs 라는 이름의 QTabWidget이 있다면
            if self.findChild(QTabWidget, 'weather_tabs'):
                self.layout().removeWidget(self.tabs_api_weather)  # 날씨 탭 제거

            # 탭 생성
            self.tabs_api_weather = QTabWidget()
            self.tabs_api_weather.setObjectName('weather_tabs')

            # 지난 날씨정보
            self.set_form_api_weather_previous_info()

            # 날씨 수직 레이아웃에 날씨 탭 추가
            self.v_layout_weather.addWidget(self.tabs_api_weather)
        except Exception as e:
            print('{set_tabs_weather} - ' + str(e))


    def set_form_api_weather_previous_info(self):
        """ API weather 지난 날씨정보 테이블 폼 세팅 """
        try:
            # 수직 레이아웃 생성
            self.v_layout_api_weather_previous_info = QVBoxLayout()

            # 데이트피커
            self.date_api_weather_previous_info = QDateEdit(calendarPopup=True)
            self.date_api_weather_previous_info.setToolTip('그저께 이상 날짜 선택 불가')
            self.date_api_weather_previous_info.setMinimumDate(QDate(1907, 10, 1))
            self.date_api_weather_previous_info.setMaximumDate(QDate(self.date_today.year(), self.date_today.month(), self.date_today.day() - 2))
            self.date_api_weather_previous_info.setDateTime(QDateTime.currentDateTime())

            # 검색 버튼
            btn_api_weather_previous_info_run = QPushButton('검색')
            btn_api_weather_previous_info_run.resize(btn_api_weather_previous_info_run.sizeHint())
            btn_api_weather_previous_info_run.clicked.connect(self.set_table_api_weather_previous_info)

            # 수직 레아이웃에 위젯 추가
            self.v_layout_api_weather_previous_info.addWidget(self.date_api_weather_previous_info)
            self.v_layout_api_weather_previous_info.addWidget(btn_api_weather_previous_info_run)
            self.v_layout_api_weather_previous_info.addSpacing(700)

            # 그룹박스 생성
            group_box_api_weather_previous_info = QGroupBox('날짜 선택')

            # 그룹박스의 레이아웃을 수직 레이아웃으로
            group_box_api_weather_previous_info.setLayout(self.v_layout_api_weather_previous_info)

            # 탭에 그룹박스 추가
            self.tabs_api_weather.addTab(group_box_api_weather_previous_info, '지난 날씨')
        except Exception as e:
            print('{set_form_api_weather_previous_info} - ' + str(e))

    def set_table_api_weather_previous_info(self):
        """ API weather 지난 날씨정보 테이블 데이터 세팅 """
        try:
            if self.v_layout_api_weather_previous_info.count() > 3:
                self.v_layout_api_weather_previous_info.removeWidget(self.table_api_weather_previous_info)
            else:
                self.v_layout_api_weather_previous_info.addSpacing(-700)

            # 테이블 컬럼 리스트 
            list_column_weather_previous_info = ['번호', '시각', '관측지점', '온도', '습도', '풍속', '강수량']

            # 요청 파라미터
            start_date = str(self.date_api_weather_previous_info.date().toPyDate()).replace('-', '')  # 시작날짜
            end_date = start_date  # 종료날짜
            weather_location = 108  # 서울로 고정

            # 요청 정보
            host = 'http://apis.data.go.kr'
            path = '/1360000/AsosHourlyInfoService/getWthrDataList'
            headers = None
            query = '?serviceKey={0}&pageNo=1&numOfRows=100&dataType=JSON&dataCd=ASOS&dateCd=HR&startDt={1}&startHh=01&endDt={2}&endHh=23&stnIds={3}'.format(
                self.data_gov_key, start_date, end_date, weather_location)
            method = 'GET'
            data = None

            # 응답
            try:
                res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)
            except Exception as e:
                raise RuntimeError("[공공데이터포털] 지난 날씨정보 요청 실패: " + str(e))

            # 응답의 바디를 json형태로 파싱
            parsed_object = json.loads(res.text)

            # 필요 데이터만 가져옴
            list_weather_previous_info = parsed_object['response']['body']['items']['item']

            # 테이블 생성
            self.table_api_weather_previous_info = QTableWidget(len(list_weather_previous_info) + 1, len(list_column_weather_previous_info), self)
            self.table_api_weather_previous_info.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.table_api_weather_previous_info.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.table_api_weather_previous_info.horizontalHeader().setVisible(False)
            self.table_api_weather_previous_info.verticalHeader().setVisible(False)

            # 컬럼 세팅
            for i, component in enumerate(list_column_weather_previous_info):
                item_column_weather_previous_info = QTableWidgetItem(component)
                item_column_weather_previous_info.setFont(self.font_header)
                item_column_weather_previous_info.setBackground(QColor(200, 200, 200))
                item_column_weather_previous_info.setTextAlignment(Qt.AlignCenter)
                self.table_api_weather_previous_info.setItem(0, i, item_column_weather_previous_info)

            # 데이터 세팅
            for i, component in enumerate(list_weather_previous_info):
                ex_weather_index = component['rnum']
                ex_weather_date = component['tm']
                ex_weather_station_name = component['stnNm']
                ex_weather_temperature = component['ta']
                ex_weather_humidity = component['hm']
                ex_weather_wind_speed = component['ws']
                ex_weather_rainfall = '0.0' if not component['rn'] else component['rn']

                item_ex_weather_index = QTableWidgetItem(ex_weather_index)
                item_ex_weather_index.setFont(self.font_content)
                item_ex_weather_date = QTableWidgetItem(ex_weather_date)
                item_ex_weather_date.setFont(self.font_content)
                item_ex_weather_station_name = QTableWidgetItem(ex_weather_station_name)
                item_ex_weather_station_name.setFont(self.font_content)
                item_ex_weather_temperature = QTableWidgetItem(ex_weather_temperature)
                item_ex_weather_temperature.setFont(self.font_content)
                item_ex_weather_humidity = QTableWidgetItem(ex_weather_humidity)
                item_ex_weather_humidity.setFont(self.font_content)
                item_ex_weather_wind_speed = QTableWidgetItem(ex_weather_wind_speed)
                item_ex_weather_wind_speed.setFont(self.font_content)
                item_ex_weather_rainfall = QTableWidgetItem(ex_weather_rainfall)
                item_ex_weather_rainfall.setFont(self.font_content)

                # 컬럼 수만큼 반복
                for j in range(len(list_column_weather_previous_info)):
                    self.table_api_weather_previous_info.setItem(i + 1, j, item_ex_weather_index)
                    self.table_api_weather_previous_info.setItem(i + 1, j + 1, item_ex_weather_date)
                    self.table_api_weather_previous_info.setItem(i + 1, j + 2, item_ex_weather_station_name)
                    self.table_api_weather_previous_info.setItem(i + 1, j + 3, item_ex_weather_temperature)
                    self.table_api_weather_previous_info.setItem(i + 1, j + 4, item_ex_weather_humidity)
                    self.table_api_weather_previous_info.setItem(i + 1, j + 5, item_ex_weather_wind_speed)
                    self.table_api_weather_previous_info.setItem(i + 1, j + 6, item_ex_weather_rainfall)

            # 레이아웃에 테이블 추가
            self.v_layout_api_weather_previous_info.addWidget(self.table_api_weather_previous_info)
        except Exception as e:
            print('{set_table_api_weather_previous_info} - ' + str(e))
