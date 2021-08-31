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


class MovieWidget(QWidget):
    """ inwoo app movie widget """

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

            # 오늘날짜
            self.date_today = QDate().currentDate()

            # 폰트
            self.font_header = QFont()  # 헤더용 폰트 객체 생성
            self.font_header.setBold(True)  # 굵게
            self.font_header.setPointSize(8)  # 글자 포인트

            self.font_content = QFont()  # 내용물 폰트 객체 생성
            self.font_content.setPointSize(8)  # 글자 포인트

            # 영화 수직 레이아웃 생성
            self.v_layout_movie = QVBoxLayout()
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

    def set_tabs_movie(self):
        """ 영화 탭 메뉴 생성 """
        try:
            # 메인 위젯의 레이아웃을 영화 수직 레이아웃으로 지정
            self.setLayout(self.v_layout_movie)
            # movie_tabs 라는 이름을 가진 QTabWidget이 있다면
            if self.findChild(QTabWidget, 'movie_tabs'):
                self.layout().removeWidget(self.tabs_api_movie)  # 탭 제거

            # 탭 생성
            self.tabs_api_movie = QTabWidget()
            self.tabs_api_movie.setObjectName('movie_tabs')

            # 박스오피스
            self.set_form_api_movie_box_office()
            # 영화정보
            self.set_form_api_movie_info()
            # 영화인
            self.set_form_api_movie_person()

            # 영화 수직 레이아웃에 위젯 추가
            self.v_layout_movie.addWidget(self.tabs_api_movie)
        except Exception as e:
            print('{set_tabs_movie} - ' + str(e))

    def set_form_api_movie_box_office(self):
        """ API movie 박스오피스 탭 폼 지정 """
        try:
            # 수직 레이아웃 생성
            self.v_layout_api_movie_box_office = QVBoxLayout()

            # 데이트픽커 위젯
            self.date_api_movie_box_office = QDateEdit(calendarPopup=True)  # 달력팝업
            self.date_api_movie_box_office.setToolTip('오늘자 이상 날짜 입력 불가')  # 툴팁
            self.date_api_movie_box_office.setMinimumDate(QDate(2003, 11, 11))  # 선택가능 최소날짜
            self.date_api_movie_box_office.setMaximumDate(QDate(self.date_today.year(), self.date_today.month(), self.date_today.day() - 1))  # 선택가능 최대날짜(오늘날짜 -1)
            self.date_api_movie_box_office.setDateTime(QDateTime.currentDateTime())  # 오늘날짜로 설정

            # 검색버튼 위젯
            btn_api_movie_box_office_run = QPushButton('검색')  # 검색버튼 생성(텍스트)
            btn_api_movie_box_office_run.resize(btn_api_movie_box_office_run.sizeHint())  # 윈도우 사이즈에 맞게 알아서 버튼크기 조절(?)
            btn_api_movie_box_office_run.clicked.connect(self.set_table_api_movie_box_office)  # 클릭 이벤트 핸들러 지정

            # 수평 레이아웃에 위젯 추가
            self.v_layout_api_movie_box_office.addWidget(self.date_api_movie_box_office)
            self.v_layout_api_movie_box_office.addWidget(btn_api_movie_box_office_run)
            self.v_layout_api_movie_box_office.addSpacing(700)  # 여백 추가

            # 날짜 그룹박스 위젯
            group_box_api_movie_box_office = QGroupBox('날짜 선택')

            # 그룹박스의 레이아웃을 v레이아웃으로
            group_box_api_movie_box_office.setLayout(self.v_layout_api_movie_box_office)

            # 탭에 위젯 추가
            self.tabs_api_movie.addTab(group_box_api_movie_box_office, '박스오피스')
        except Exception as e:
            print('{set_form_api_movie_box_office} - ' + str(e))

    def set_table_api_movie_box_office(self):
        """ API movie 박스오피스 탭 테이블에 데이터 지정 """
        try:
            # 레이아웃의 위젯 개수가 3보다 크다면(최초 검색이 아니라면)
            if self.v_layout_api_movie_box_office.count() > 3:
                self.v_layout_api_movie_box_office.removeWidget(self.table_api_movie_box_office)  # 기존 테이블 제거
            else:
                self.v_layout_api_movie_box_office.addSpacing(-700)  # 여백 제거

            # 박스오피스 컬럼
            list_column_box_office = ['순위', '개봉일', '누적매출액(\\)', '누적관객수', '해당일자 상영일수', '제목']

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
                item_column_box_office.setBackground(QColor(200, 200, 200))
                self.table_api_movie_box_office.setItem(0, i, item_column_box_office)

            # 내용(데이터) 지정
            # 데이터 개수만큼 반복
            for i, component in enumerate(list_box_office):
                movie_rank = str(component['rank'])
                movie_open_date = str(component['openDt'])
                movie_sales_account = format(int(component['salesAcc']), ',')
                movie_audience_account = format(int(component['audiAcc']), ',')
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
            self.v_layout_api_movie_box_office.addWidget(self.table_api_movie_box_office)

        except Exception as e:
            print('{set_table_api_movie_box_office} - ' + str(e))

    def set_form_api_movie_info(self):
        """ API movie 영화정보 탭 폼 지정 """
        try:
            # 수직 레이아웃 생성
            self.v_layout_api_movie_info = QVBoxLayout()

            # 인풋란 위젯
            self.line_edit_api_movie_info = QLineEdit()  # 입력란
            self.line_edit_api_movie_info.setPlaceholderText('영화제목 입력 (검색결과 선택 시 상세정보 노출)')  # 플레이스홀더
            # self.line_edit_api_movie_info.setToolTip('영화제목 입력')  # 툴팁

            # 검색버튼 위젯
            btn_api_movie_info_run = QPushButton('검색')  # 검색버튼 생성(텍스트)
            btn_api_movie_info_run.resize(btn_api_movie_info_run.sizeHint())  # 윈도우 사이즈에 맞게 알아서 버튼크기 조절(?)
            btn_api_movie_info_run.clicked.connect(self.set_table_api_movie_info)  # 클릭 이벤트 핸들러 지정

            # 수직 레이아웃에 위젯 추가
            self.v_layout_api_movie_info.addWidget(self.line_edit_api_movie_info)
            self.v_layout_api_movie_info.addWidget(btn_api_movie_info_run)
            self.v_layout_api_movie_info.addSpacing(700)

            # 날짜 그룹박스 위젯
            group_box_api_movie_info = QGroupBox('제목 입력')

            # 그룹박스의 레이아웃을 v레이아웃으로
            group_box_api_movie_info.setLayout(self.v_layout_api_movie_info)

            # 탭에 위젯 추가
            self.tabs_api_movie.addTab(group_box_api_movie_info, '영화정보')
        except Exception as e:
            print('{set_form_api_movie_info} - ' + str(e))

    def set_table_api_movie_info(self):
        """ API movie 영화정보 테이블에 데이터 지정 """
        try:
            # 레이아웃의 위젯 개수가 5개 초과라면(영화정보 최초 실행이 아니라면)
            if self.v_layout_api_movie_info.count() == 5:
                self.v_layout_api_movie_info.removeWidget(self.table_api_movie_info)  # 결과 테이블 제거
            # 레이아웃의 위젯 개수가 5개 초과라면(영화상세정보 최초 실행이 아니라면)
            elif self.v_layout_api_movie_info.count() > 5:
                self.v_layout_api_movie_info.removeWidget(self.table_api_movie_info)  # 결과 테이블 제거
                self.v_layout_api_movie_info.removeWidget(self.table_api_movie_info_detail)  # 결과 테이블 제거
            else:
                self.v_layout_api_movie_info.addSpacing(-700)  # 여백 제거

            # 영화정보 컬럼
            list_column_movie_info = ['번호', '제목', '제작연도', '국내 개봉일', '장르', '국가', '감독']

            # 입력된 검색 영화제목명
            searched_movie_name = str(self.line_edit_api_movie_info.text())

            # 요청 정보
            host = 'http://kobis.or.kr'
            path = '/kobisopenapi/webservice/rest/movie/searchMovieList.json'
            headers = None
            query = '?key={0}&movieNm={1}'.format(self.kofic_key, searched_movie_name)
            method = 'GET'
            data = None

            # 응답
            try:
                res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)
            except Exception as e:
                raise RuntimeError("[영화진흥위원회] 영화 목록 정보 요청 실패: " + str(e))

            # 응답의 바디를 json형태로 파싱
            parsed_object = json.loads(res.text)

            # 조회 결과
            dict_movie_result = parsed_object['movieListResult']

            # 검색영화 리스트만 가져옴
            list_movie_search = dict_movie_result['movieList']

            # 검색 개수가 0개라면
            if not list_movie_search:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("알림")
                msg.setText('검색 결과가 없습니다.')
                msg.exec_()

            # 영화상세정보를 검색하기 위해 영화코드를 저장할 리스트
            self.list_movie_code = []

            # 테이블 생성
            self.table_api_movie_info = QTableWidget(len(list_movie_search) + 1, len(list_column_movie_info), self)  # 데이터 행x컬럼 열 크기의 테이블 생성
            self.table_api_movie_info.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 데이터 수정 불가능
            self.table_api_movie_info.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 테이블 너비를 윈도우 너비에 맞춤
            self.table_api_movie_info.horizontalHeader().setVisible(False)  # 수평 헤더 숨김
            self.table_api_movie_info.verticalHeader().setVisible(False)  # 수직 헤더 숨김
            self.table_api_movie_info.setStatusTip('클릭 시 영화 상세정보 노출')  # 하단 상태표시줄

            # 컬럼 지정
            for i, component in enumerate(list_column_movie_info):
                item_column_movie_info = QTableWidgetItem(component)
                item_column_movie_info.setFont(self.font_header)
                item_column_movie_info.setBackground(QColor(200, 200, 200))
                self.table_api_movie_info.setItem(0, i, item_column_movie_info)

            # 결과출력
            for i, component in enumerate(list_movie_search):
                movie_code = component['movieCd']
                self.list_movie_code.append(movie_code)

                movie_name_kor = component['movieNm']
                movie_prod_year = component['prdtYear']
                movie_open_date = component['openDt']
                movie_genre = component['genreAlt']
                movie_prod_nation = component['repNationNm']
                list_movie_director = component['directors']
                movie_director = 'unknown' if not list_movie_director else list_movie_director[0]['peopleNm']

                item_movie_num = QTableWidgetItem(str(i + 1))
                item_movie_num.setFont(self.font_content)
                item_movie_name_kor = QTableWidgetItem(movie_name_kor)
                item_movie_name_kor.setFont(self.font_content)
                item_movie_prod_year = QTableWidgetItem(movie_prod_year)
                item_movie_prod_year.setFont(self.font_content)
                item_movie_open_date = QTableWidgetItem(movie_open_date)
                item_movie_open_date.setFont(self.font_content)
                item_movie_genre = QTableWidgetItem(movie_genre)
                item_movie_genre.setFont(self.font_content)
                item_movie_prod_nation = QTableWidgetItem(movie_prod_nation)
                item_movie_prod_nation.setFont(self.font_content)
                item_movie_director = QTableWidgetItem(movie_director)
                item_movie_director.setFont(self.font_content)

                # 컬럼 개수만큼 반복
                for j in range(len(list_column_movie_info)):
                    self.table_api_movie_info.setItem(i + 1, j, item_movie_num)
                    self.table_api_movie_info.setItem(i + 1, j + 1, item_movie_name_kor)
                    self.table_api_movie_info.setItem(i + 1, j + 2, item_movie_prod_year)
                    self.table_api_movie_info.setItem(i + 1, j + 3, item_movie_open_date)
                    self.table_api_movie_info.setItem(i + 1, j + 4, item_movie_genre)
                    self.table_api_movie_info.setItem(i + 1, j + 5, item_movie_prod_nation)
                    self.table_api_movie_info.setItem(i + 1, j + 6, item_movie_director)

            self.table_api_movie_info.clicked.connect(self.set_table_api_movie_info_detail)

            # 현재 레이아웃에 테이블 위젯 추가
            self.v_layout_api_movie_info.addWidget(self.table_api_movie_info)
        except Exception as e:
            print('{set_table_api_movie_info} - ' + str(e))

    def set_table_api_movie_info_detail(self):
        """ API movie 영화상세정보 테이블에 데이터 지정 """
        try:
            # 레이아웃의 위젯 개수가 5개 초과라면(영화상세정보 최초 실행이 아니라면)
            if self.v_layout_api_movie_info.count() > 5:
                self.v_layout_api_movie_info.removeWidget(self.table_api_movie_info_detail)  # 결과 테이블 제거
            # else:
            #     self.v_layout_api_movie_info.addSpacing(-700)  # 여백 제거

            # 영화정보 컬럼
            list_column_movie_info_detail = ['제목(국문)', '제목(영문)', '러닝타임(분)', '제작연도', '개봉일자', '감독']

            # 클릭된 영화의 행번호
            clicked_movie_row = self.table_api_movie_info.currentIndex().row()

            if not clicked_movie_row:
                return

            # 요청 정보
            host = 'http://www.kobis.or.kr'
            path = '/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
            headers = None
            query = '?key={0}&movieCd={1}'.format(self.kofic_key, self.list_movie_code[clicked_movie_row - 1])
            method = 'GET'
            data = None

            # 응답
            try:
                res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)
            except Exception as e:
                raise RuntimeError("[영화진흥위원회] 영화 상세정보 요청 실패: " + str(e))

            # 응답의 바디를 json형태로 파싱
            parsed_object = json.loads(res.text)

            movie_info_dict = parsed_object['movieInfoResult']['movieInfo']

            # 테이블 생성
            self.table_api_movie_info_detail = QTableWidget(2, len(list_column_movie_info_detail), self)  # 2행x열개수 크기의 테이블 생성
            self.table_api_movie_info_detail.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 데이터 수정 불가능
            self.table_api_movie_info_detail.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 테이블 너비를 윈도우 너비에 맞춤
            self.table_api_movie_info_detail.horizontalHeader().setVisible(False)  # 수평 헤더 숨김
            self.table_api_movie_info_detail.verticalHeader().setVisible(False)  # 수직 헤더 숨김

            # 컬럼 지정
            for i, component in enumerate(list_column_movie_info_detail):
                item_column_movie_info_detail = QTableWidgetItem(component)
                item_column_movie_info_detail.setFont(self.font_header)
                item_column_movie_info_detail.setBackground(QColor(200, 200, 200))
                self.table_api_movie_info_detail.setItem(0, i, item_column_movie_info_detail)

            detail_movie_movie_name_kor = movie_info_dict['movieNm']
            detail_movie_movie_name_eng = movie_info_dict['movieNmEn']
            detail_movie_movie_show_time = movie_info_dict['showTm']
            detail_movie_movie_prod_year = movie_info_dict['prdtYear']
            detail_movie_movie_open_date = movie_info_dict['openDt']
            list_detail_movie_movie_directors = movie_info_dict['directors']
            detail_movie_movie_director = 'unknown' if not list_detail_movie_movie_directors else list_detail_movie_movie_directors[0]['peopleNm']

            item_detail_movie_movie_name_kor = QTableWidgetItem(detail_movie_movie_name_kor)
            item_detail_movie_movie_name_kor.setFont(self.font_content)
            item_detail_movie_movie_name_eng = QTableWidgetItem(detail_movie_movie_name_eng)
            item_detail_movie_movie_name_eng.setFont(self.font_content)
            item_detail_movie_movie_show_time = QTableWidgetItem(detail_movie_movie_show_time)
            item_detail_movie_movie_show_time.setFont(self.font_content)
            item_detail_movie_movie_prod_year = QTableWidgetItem(detail_movie_movie_prod_year)
            item_detail_movie_movie_prod_year.setFont(self.font_content)
            item_detail_movie_movie_open_date = QTableWidgetItem(detail_movie_movie_open_date)
            item_detail_movie_movie_open_date.setFont(self.font_content)
            item_detail_movie_movie_director = QTableWidgetItem(detail_movie_movie_director)
            item_detail_movie_movie_director.setFont(self.font_content)

            self.table_api_movie_info_detail.setItem(1, 0, item_detail_movie_movie_name_kor)
            self.table_api_movie_info_detail.setItem(1, 1, item_detail_movie_movie_name_eng)
            self.table_api_movie_info_detail.setItem(1, 2, item_detail_movie_movie_show_time)
            self.table_api_movie_info_detail.setItem(1, 3, item_detail_movie_movie_prod_year)
            self.table_api_movie_info_detail.setItem(1, 4, item_detail_movie_movie_open_date)
            self.table_api_movie_info_detail.setItem(1, 5, item_detail_movie_movie_director)

            # 현재 레이아웃에 테이블 위젯 추가
            self.v_layout_api_movie_info.addWidget(self.table_api_movie_info_detail)

        except Exception as e:
            print('{set_table_api_movie_info_detail} - ' + str(e))


    def set_form_api_movie_person(self):
        """ API movie 영화인 탭 폼 지정 """
        try:
            # 수직 레이아웃 생성
            self.v_layout_api_movie_person = QVBoxLayout()

            # 인풋란 위젯
            self.line_edit_api_movie_person = QLineEdit()  # 입력란
            self.line_edit_api_movie_person.setPlaceholderText('영화인 이름 입력')  # 플레이스홀더
            # self.line_edit_api_movie_person.setToolTip('영화인 이름 입력')  # 툴팁

            # 검색버튼 위젯
            btn_api_movie_person_run = QPushButton('검색')  # 검색버튼 생성(텍스트)
            btn_api_movie_person_run.resize(btn_api_movie_person_run.sizeHint())  # 윈도우 사이즈에 맞게 알아서 버튼크기 조절(?)
            btn_api_movie_person_run.clicked.connect(self.set_table_api_movie_person)  # 클릭 이벤트 핸들러 지정

            # 수직 레이아웃에 위젯 추가
            self.v_layout_api_movie_person.addWidget(self.line_edit_api_movie_person)
            self.v_layout_api_movie_person.addWidget(btn_api_movie_person_run)
            self.v_layout_api_movie_person.addSpacing(700)

            # 날짜 그룹박스 위젯
            group_box_api_movie_person = QGroupBox('이름 입력')

            # 그룹박스의 레이아웃을 v레이아웃으로
            group_box_api_movie_person.setLayout(self.v_layout_api_movie_person)

            # 탭에 위젯 추가
            self.tabs_api_movie.addTab(group_box_api_movie_person, '영화인')
        except Exception as e:
            print('{set_form_api_movie_person} - ' + str(e))

    def set_table_api_movie_person(self):
        """ API movie 영화인 테이블에 데이터 지정 """
        try:
            # 레이아웃의 위젯 개수가 3개 초과라면(영화인 최초 실행이 아니라면)
            if self.v_layout_api_movie_person.count() > 3:
                self.v_layout_api_movie_person.removeWidget(self.table_api_movie_person)  # 결과 테이블 제거
            else:
                self.v_layout_api_movie_person.addSpacing(-700)  # 여백 제거

            # 영화인 컬럼
            list_column_movie_person = ['번호', '이름(국문)', '이름(영문)', '역할', '필모그래피']

            # 입력된 검색 영화인 이름
            searched_movie_person_name = str(self.line_edit_api_movie_person.text())

            # 요청 정보
            host = 'http://www.kobis.or.kr'
            path = '/kobisopenapi/webservice/rest/people/searchPeopleList.json'
            headers = None
            query = '?key={0}&peopleNm={1}'.format(self.kofic_key, searched_movie_person_name)
            method = 'GET'
            data = None

            # 응답
            try:
                res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query,
                                                                   method=method, data=data)
            except Exception as e:
                raise RuntimeError("[영화진흥위원회] 영화 목록 정보 요청 실패: " + str(e))

            # 응답의 바디를 json형태로 파싱
            parsed_object = json.loads(res.text)

            # 검색 결과
            dict_people_result = parsed_object['peopleListResult']

            # 영화인 리스트만 가져옴
            list_people_search = dict_people_result['peopleList']

            # 검색 개수가 0개라면
            if not list_people_search:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("알림")
                msg.setText('검색 결과가 없습니다.')
                msg.exec_()

            # 테이블 생성
            self.table_api_movie_person = QTableWidget(len(list_people_search) + 1, len(list_column_movie_person),self)  # 데이터 행x컬럼 열 크기의 테이블 생성
            self.table_api_movie_person.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 데이터 수정 불가능
            self.table_api_movie_person.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  # 테이블 너비를 윈도우 너비에 맞춤, 데이터 값에 따라 컬럼 크기 자동 조절
            self.table_api_movie_person.horizontalHeader().setVisible(False)  # 수평 헤더 숨김
            self.table_api_movie_person.verticalHeader().setVisible(False)  # 수직 헤더 숨김
            # 컬럼 당 비율 지정
            # self.table_api_movie_person.setColumnWidth(0, self.width() * 1 / 10)
            # self.table_api_movie_person.setColumnWidth(1, self.width() * 2 / 10)
            # self.table_api_movie_person.setColumnWidth(2, self.width() * 2 / 10)
            # self.table_api_movie_person.setColumnWidth(3, self.width() * 1 / 10)
            # self.table_api_movie_person.setColumnWidth(4, self.width() * 5 / 10)

            # 컬럼 지정
            for i, component in enumerate(list_column_movie_person):
                item_column_movie_person = QTableWidgetItem(component)
                item_column_movie_person.setFont(self.font_header)
                item_column_movie_person.setBackground(QColor(200, 200, 200))
                self.table_api_movie_person.setItem(0, i, item_column_movie_person)

            # 결과출력
            for i, component in enumerate(list_people_search):
                people_name_kor = component['peopleNm']
                people_name_eng = component['peopleNmEn']
                people_role_name = component['repRoleNm']
                people_filmography_names = component['filmoNames']

                item_people_name_num = QTableWidgetItem(str(i + 1))
                item_people_name_num.setFont(self.font_content)
                item_people_name_kor = QTableWidgetItem(people_name_kor)
                item_people_name_kor.setFont(self.font_content)
                item_people_name_eng = QTableWidgetItem(people_name_eng)
                item_people_name_eng.setFont(self.font_content)
                item_people_role_name = QTableWidgetItem(people_role_name)
                item_people_role_name.setFont(self.font_content)
                item_people_filmography_names = QTableWidgetItem(people_filmography_names)
                item_people_filmography_names.setFont(self.font_content)

                # 컬럼 개수만큼 반복
                for j in range(len(list_column_movie_person)):
                    self.table_api_movie_person.setItem(i + 1, j, item_people_name_num)
                    self.table_api_movie_person.setItem(i + 1, j + 1, item_people_name_kor)
                    self.table_api_movie_person.setItem(i + 1, j + 2, item_people_name_eng)
                    self.table_api_movie_person.setItem(i + 1, j + 3, item_people_role_name)
                    self.table_api_movie_person.setItem(i + 1, j + 4, item_people_filmography_names)

            # 현재 레이아웃에 테이블 위젯 추가
            self.v_layout_api_movie_person.addWidget(self.table_api_movie_person)
        except Exception as e:
            print('{set_table_api_movie_person} - ' + str(e))
