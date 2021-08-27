import sys
import time
import datetime
import json
import jproperties

from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Classes.Util.Logger import logger

from Classes.Util.UnicodeUtil import UnicodeUtil
from Classes.Util.TransmitterReceiver import TransmitterReceiver


class InwooMainWidget(QWidget):
    """ inwoo app main widget """

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

            # 영화 키
            self.kofic_key = self.property_reader.get('KOFIC_KEY').data

            # 각 메뉴의 상세메뉴 초기화
            self.list_movie_menu = ['박스오피스', '영화', '영화인']

            # 오늘날짜
            self.date_today = QDate().currentDate()

            # 폰트
            self.font_header = QFont()  # 헤더용 폰트 객체 생성
            self.font_header.setBold(True)  # 굵게
            self.font_header.setPointSize(8)  # 글자 포인트

            self.font_content = QFont()  # 내용물 폰트 객체 생성
            self.font_content.setPointSize(8)  # 글자 포인트

            # 수직 레이아웃 생성
            self.v_layout_01 = QVBoxLayout()

            # 현재 위젯의 레이아웃 지정
            self.setLayout(self.v_layout_01)
        except Exception as e:
            print('{init_ui} - ' + str(e))

    def date_picker_handler(self):
        """ 대출일 날짜 변경 시 이벤트 핸들러 """
        try:
            # 각 날짜 값 저장
            selected_date_picker_01 = self.date_picker_01.date()
            selected_date_picker_02 = self.date_picker_02.date()

            self.date_picker_01.setMaximumDate(selected_date_picker_02)  # 시작 대출일 최대치를 끝 대출일 선택값으로
            self.date_picker_02.setMinimumDate(selected_date_picker_01)  # 끝 대출일 최소치를 시작 대출일 선택값으로
        except Exception as e:
            print('{date_picker_handler} - ' + str(e))

    def set_tabs_movie(self):
        """ 영화 탭 메뉴 생성 """
        try:
            # 레이아웃의 위젯 개수가 0보다 크다면(최초 실행이 아니라면)
            if self.layout().count() > 0:
                self.layout().removeWidget(self.tabs_api_movie)  # 탭 제거

            # 수평 레이아웃 생성
            h_layout_api_movie_box_office = QHBoxLayout()

            # 데이트픽커 위젯
            self.date_api_movie_box_office = QDateEdit(calendarPopup=True)  # 달력팝업
            self.date_api_movie_box_office.setToolTip('오늘자 이상 날짜 입력 불가')  # 툴팁
            self.date_api_movie_box_office.setMinimumDate(QDate(2010, 1, 1))  # 선택가능 최소날짜
            self.date_api_movie_box_office.setMaximumDate(QDate(self.date_today.year(), self.date_today.month(), self.date_today.day() - 1))  # 선택가능 최대날짜(오늘날짜 -1)
            self.date_api_movie_box_office.setDateTime(QDateTime.currentDateTime())  # 오늘날짜로 설정

            # 실행버튼 위젯
            btn_api_movie_box_office_run = QPushButton('검색')  # 검색버튼 생성(텍스트)
            btn_api_movie_box_office_run.resize(btn_api_movie_box_office_run.sizeHint())  # 윈도우 사이즈에 맞게 알아서 버튼크기 조절(?)
            btn_api_movie_box_office_run.clicked.connect(self.set_table_api_movie_box_office)  # 클릭 시 quit함수에 연결(종료)

            # 수평 레이아웃에 위젯 추가
            h_layout_api_movie_box_office.addWidget(self.date_api_movie_box_office)
            h_layout_api_movie_box_office.addWidget(btn_api_movie_box_office_run)
            h_layout_api_movie_box_office.addSpacing(1000)

            # 날짜 그룹박스 위젯
            group_box_api_movie_box_office = QGroupBox('날짜 선택')

            # 그룹박스의 레이아웃을 h레이아웃으로
            group_box_api_movie_box_office.setLayout(h_layout_api_movie_box_office)

            # 탭 생성
            self.tabs_api_movie = QTabWidget()

            # 탭에 위젯 추가
            self.tabs_api_movie.addTab(group_box_api_movie_box_office, '박스오피스정보')
            self.tabs_api_movie.addTab(group_box_api_movie_box_office, '영화정보')
            self.tabs_api_movie.addTab(group_box_api_movie_box_office, '영화인정보')

            # 수직 레이아웃에 위젯 추가
            self.v_layout_01.addWidget(self.tabs_api_movie)
        except Exception as e:
            print('{set_tabs_movie} - ' + str(e))

    def set_table_api_movie_box_office(self):
        """ API movie 박스오피스 테이블에 데이터 지정 """
        try:
            # 레이아웃의 위젯 개수가 1보다 크다면(최초 검색이 아니라면)
            if self.layout().count() > 1:
                self.layout().removeWidget(self.table_api_movie_box_office)  # 테이블 제거

            # 박스오피스 컬럼
            list_column_box_office = ['순위', '개봉일', '누적매출액', '누적관객수', '해당일자 상영일수', '제목']

            # 박스오피스 검색 날짜
            selected_date = str(self.date_api_movie_box_office.date().toPyDate()).replace('-', '')

            # 요청 정보
            host = 'http://www.kobis.or.kr'
            path = '/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
            headers = None
            query = '?key={0}&targetDt={1}'.format(self.kofic_key, selected_date)
            method = 'GET'
            data = None

            # 응답
            try:
                res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)
            except Exception as e:
                raise RuntimeError("[영화진흥위원회] 박스오피스 정보 요청 실패: " + str(e))

            # 응답의 바디를 json형태로 파싱
            parsed_object = json.loads(res.text)

            # 박스오피스 리스트만 가져옴
            list_box_office = parsed_object['boxOfficeResult']['dailyBoxOfficeList']

            # 테이블 생성
            self.table_api_movie_box_office = QTableWidget(len(list_box_office) + 1, len(list_column_box_office), self)  # 데이터 행x컬럼 열 크기의 테이블 생성
            self.table_api_movie_box_office.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 데이터 수정 불가능
            self.table_api_movie_box_office.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 테이블 너비를 윈도우 너비에 맞춤
            self.table_api_movie_box_office.horizontalHeader().setVisible(False)  # 수평 헤더 숨김
            self.table_api_movie_box_office.verticalHeader().setVisible(False)  # 수직 헤더 숨김

            # 컬럼 지정
            for i, component in enumerate(list_column_box_office):
                item_column_box_office = QTableWidgetItem(component)
                item_column_box_office.setFont(self.font_header)
                self.table_api_movie_box_office.setItem(0, i, item_column_box_office)

            # 내용(데이터) 지정
            # 데이터 개수만큼 반복
            for i, component in enumerate(list_box_office):
                movie_rank = str(component['rank'])
                movie_open_date = str(component['openDt'])
                movie_sales_account = str(component['salesAcc'])
                movie_audience_account = str(component['audiAcc'])
                movie_show_count = str(component['showCnt'])
                movie_name = str(component['movieNm'])

                item_movie_rank = QTableWidgetItem(movie_rank)
                item_movie_rank.setFont(self.font_content)
                item_movie_open_date = QTableWidgetItem(movie_open_date)
                item_movie_open_date.setFont(self.font_content)
                item_sales_account = QTableWidgetItem(movie_sales_account)
                item_sales_account.setFont(self.font_content)
                item_audience_account = QTableWidgetItem(movie_audience_account)
                item_audience_account.setFont(self.font_content)
                item_show_count = QTableWidgetItem(movie_show_count)
                item_show_count.setFont(self.font_content)
                item_movie_name = QTableWidgetItem(movie_name)
                item_movie_name.setFont(self.font_content)
                # 컬럼 개수만큼 반복
                for j in range(len(list_column_box_office)):
                    self.table_api_movie_box_office.setItem(i + 1, j, item_movie_rank)
                    self.table_api_movie_box_office.setItem(i + 1, j + 1, item_movie_open_date)
                    self.table_api_movie_box_office.setItem(i + 1, j + 2, item_sales_account)
                    self.table_api_movie_box_office.setItem(i + 1, j + 3, item_audience_account)
                    self.table_api_movie_box_office.setItem(i + 1, j + 4, item_show_count)
                    self.table_api_movie_box_office.setItem(i + 1, j + 5, item_movie_name)

            # 현재 레이아웃에 테이블 위젯 추가
            self.layout().addWidget(self.table_api_movie_box_office)

        except Exception as e:
            print('{set_table_api_movie_box_office} - ' + str(e))

