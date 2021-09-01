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


class Covid19Widget(QWidget):
    """ inwoo app covid19 widget """

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

            # 코로나 수직 레이아웃 생성
            self.v_layout_covid19 = QVBoxLayout()
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

    def set_tabs_covid19(self):
        """ 코로나19 메뉴 탭 생성 """
        try:
            # 메인 위젯의 레이아웃을 코로나 수직 레이아웃으로 지정
            self.setLayout(self.v_layout_covid19)

            # covid19_tabs 라는 이름의 QTabWidget이 있다면
            if self.findChild(QTabWidget, 'covid19_tabs'):
                self.layout().removeWidget(self.tabs_api_covid19)  # 코로나19 탭 제거

            # 탭 생성
            self.tabs_api_covid19 = QTabWidget()
            self.tabs_api_covid19.setObjectName('covid19_tabs')

            # 국내 센터 정보
            self.set_form_api_covid19_korea_center()

            # 국가별 이슈
            self.set_form_api_covid19_national_issue()

            # 코로나19 수직 레이아웃에 코로나19 탭 추가
            self.v_layout_covid19.addWidget(self.tabs_api_covid19)
        except Exception as e:
            print('{set_tabs_covid19} - ' + str(e))


    def set_form_api_covid19_korea_center(self):
        """ API covid19 국내 센터정보 테이블 폼 세팅 """
        try:
            # 수직 레이아웃 생성
            self.v_layout_api_covid19_korea_center = QVBoxLayout()

            # 입력란
            self.line_edit_api_covid19_korea_center = QLineEdit()
            self.line_edit_api_covid19_korea_center.setPlaceholderText('검색할 지역을 입력해 주세요(미 입력 시 전체)')

            # 검색 버튼
            btn_api_covid19_korea_center_run = QPushButton('검색')
            btn_api_covid19_korea_center_run.resize(btn_api_covid19_korea_center_run.sizeHint())
            btn_api_covid19_korea_center_run.clicked.connect(self.set_table_api_covid19_korea_center)

            # 수직 레아이웃에 위젯 추가
            self.v_layout_api_covid19_korea_center.addWidget(self.line_edit_api_covid19_korea_center)
            self.v_layout_api_covid19_korea_center.addWidget(btn_api_covid19_korea_center_run)
            self.v_layout_api_covid19_korea_center.addSpacing(700)

            # 그룹박스 생성
            group_box_api_covid19_korea_center = QGroupBox('지역 입력')
            # 그룹박스의 레이아웃을 수직 레이아웃으로
            group_box_api_covid19_korea_center.setLayout(self.v_layout_api_covid19_korea_center)

            # 탭에 그룹박스 추가
            self.tabs_api_covid19.addTab(group_box_api_covid19_korea_center, '국내 센터정보')
        except Exception as e:
            print('{set_form_api_covid19_korea_center} - ' + str(e))

    def set_table_api_covid19_korea_center(self):
        """ API covid19 국내 센터정보 테이블 데이터 세팅 """
        try:
            if self.v_layout_api_covid19_korea_center.count() > 3:
                self.v_layout_api_covid19_korea_center.removeWidget(self.table_api_covid19_korea_center)
            else:
                self.v_layout_api_covid19_korea_center.addSpacing(-700)

            # 테이블 컬럼 리스트 
            list_column_covid19_korea_center = ['센터번호', '센터명', '시설명', '주소', '우편번호']

            # 지역 입력 값
            searched_location_value = str(self.line_edit_api_covid19_korea_center.text().strip())

            # 요청 정보
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
                raise RuntimeError("[공공데이터포털] 코로나19 국내 센터정보 요청 실패: " + str(e))

            # 응답의 바디를 json형태로 파싱
            parsed_object = json.loads(res.text)

            # 필요 데이터만 가져옴
            center_count = parsed_object['totalCount']
            list_covid19_korea_center = parsed_object['data']

            # 검색 결과가 포함된 결과 개수
            result_count = 0

            # 검색 결과가 포함된 결과 개수 조회
            for i, component in enumerate(list_covid19_korea_center):
                center_name = component['centerName']
                center_address = component['address']
                center_facility_name = component['facilityName']
                if searched_location_value in center_name or searched_location_value in center_address or searched_location_value in center_facility_name:
                    result_count += 1

            # 테이블 생성
            self.table_api_covid19_korea_center = QTableWidget(result_count + 1, len(list_column_covid19_korea_center), self)
            self.table_api_covid19_korea_center.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.table_api_covid19_korea_center.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.table_api_covid19_korea_center.horizontalHeader().setVisible(False)
            self.table_api_covid19_korea_center.verticalHeader().setVisible(False)

            # 컬럼 세팅
            for i, component in enumerate(list_column_covid19_korea_center):
                item_column_covid19_korea_center = QTableWidgetItem(component)
                item_column_covid19_korea_center.setFont(self.font_header)
                item_column_covid19_korea_center.setBackground(QColor(200, 200, 200))
                item_column_covid19_korea_center.setTextAlignment(Qt.AlignCenter)
                self.table_api_covid19_korea_center.setItem(0, i, item_column_covid19_korea_center)

            # 데이터를 입력하 테이블 행번호로 사용하기 위해 다시 0으로 초기화
            result_count = 0

            # 데이터 세팅
            for i, component in enumerate(list_covid19_korea_center):
                center_id = str(component['id'])
                center_name = component['centerName']
                center_address = component['address']
                center_facility_name = component['facilityName']
                center_zip_code = component['zipCode']

                if searched_location_value in center_name or searched_location_value in center_address or searched_location_value in center_facility_name:
                    item_center_id = QTableWidgetItem(center_id)
                    item_center_id.setFont(self.font_content)
                    item_center_name = QTableWidgetItem(center_name)
                    item_center_name.setFont(self.font_content)
                    item_center_address = QTableWidgetItem(center_address)
                    item_center_address.setFont(self.font_content)
                    item_center_facility_name = QTableWidgetItem(center_facility_name)
                    item_center_facility_name.setFont(self.font_content)
                    item_center_zip_code = QTableWidgetItem(center_zip_code)
                    item_center_zip_code.setFont(self.font_content)

                    result_count += 1

                    # 컬럼 수만큼 반복
                    for j in range(len(list_column_covid19_korea_center)):
                        self.table_api_covid19_korea_center.setItem(result_count, j, item_center_id)
                        self.table_api_covid19_korea_center.setItem(result_count, j + 1, item_center_name)
                        self.table_api_covid19_korea_center.setItem(result_count, j + 2, item_center_facility_name)
                        self.table_api_covid19_korea_center.setItem(result_count, j + 3, item_center_address)
                        self.table_api_covid19_korea_center.setItem(result_count, j + 4, item_center_zip_code)
                else:
                    continue

            # 레이아웃에 테이블 추가
            self.v_layout_api_covid19_korea_center.addWidget(self.table_api_covid19_korea_center)
            
            # 검색결과가 없을 때
            if not result_count:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("알림")
                msg.setText('검색 결과가 없습니다')
                msg.exec_()
        except Exception as e:
            print('{set_table_api_covid19_korea_center} - ' + str(e))

    def set_form_api_covid19_national_issue(self):
        """ API covid19 국가별 이슈 테이블 폼 세팅 """
        try:
            # 수직 레이아웃 생성
            self.v_layout_api_covid19_national_issue = QVBoxLayout()

            # 입력란
            self.line_edit_api_covid19_national_issue = QLineEdit()
            self.line_edit_api_covid19_national_issue.setPlaceholderText('검색할 국가를 입력해 주세요')

            # 검색 버튼
            btn_api_covid19_national_issue_run = QPushButton('검색')
            btn_api_covid19_national_issue_run.resize(btn_api_covid19_national_issue_run.sizeHint())
            btn_api_covid19_national_issue_run.clicked.connect(self.set_table_api_covid19_national_issue)

            # 수직 레아이웃에 위젯 추가
            self.v_layout_api_covid19_national_issue.addWidget(self.line_edit_api_covid19_national_issue)
            self.v_layout_api_covid19_national_issue.addWidget(btn_api_covid19_national_issue_run)
            self.v_layout_api_covid19_national_issue.addSpacing(700)

            # 그룹박스 생성
            group_box_api_covid19_national_issue = QGroupBox('국가 입력')
            # 그룹박스의 레이아웃을 수직 레이아웃으로
            group_box_api_covid19_national_issue.setLayout(self.v_layout_api_covid19_national_issue)

            # 탭에 그룹박스 추가
            self.tabs_api_covid19.addTab(group_box_api_covid19_national_issue, '국가별 이슈')
        except Exception as e:
            print('{set_form_api_covid19_national_issue} - ' + str(e))

    def set_table_api_covid19_national_issue(self):
        """ API covid19 국가별 이슈 테이블 데이터 세팅 """
        try:
            if self.v_layout_api_covid19_national_issue.count() > 3:
                self.v_layout_api_covid19_national_issue.removeWidget(self.table_api_covid19_national_issue)
            else:
                self.v_layout_api_covid19_national_issue.addSpacing(-700)

            # 테이블 컬럼 리스트
            list_column_covid19_national_issue = ['작성일', '국가', '타이틀']

            # 국가 입력 값
            searched_nation_value = str(self.line_edit_api_covid19_national_issue.text().strip())

            # 요청 정보
            host = 'http://apis.data.go.kr'
            path = '/1262000/CountryCovid19SafetyServiceNew/getCountrySafetyNewsListNew'
            headers = None
            query = '?serviceKey={0}&numOfRows=100&pageNo=1&cond[country_nm::EQ]={1}'.format(self.data_gov_key, searched_nation_value)
            method = 'GET'
            data = None

            # 응답
            try:
                res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)
            except Exception as e:
                raise RuntimeError("[공공데이터포털] 코로나19 국가별 이슈 요청 실패: " + str(e))

            # 응답의 바디를 json형태로 파싱
            parsed_object = json.loads(res.text)

            # 필요 데이터만 가져옴
            issue_count = parsed_object['currentCount']
            list_covid19_national_issue = parsed_object['data']

            # 테이블 생성
            self.table_api_covid19_national_issue = QTableWidget(len(list_covid19_national_issue) + 1, len(list_column_covid19_national_issue), self)
            self.table_api_covid19_national_issue.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.table_api_covid19_national_issue.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.table_api_covid19_national_issue.horizontalHeader().setVisible(False)
            self.table_api_covid19_national_issue.verticalHeader().setVisible(False)

            # 컬럼 세팅
            for i, component in enumerate(list_column_covid19_national_issue):
                item_column_covid19_national_issue = QTableWidgetItem(component)
                item_column_covid19_national_issue.setFont(self.font_header)
                item_column_covid19_national_issue.setBackground(QColor(200, 200, 200))
                item_column_covid19_national_issue.setTextAlignment(Qt.AlignCenter)
                self.table_api_covid19_national_issue.setItem(0, i, item_column_covid19_national_issue)

            # 데이터 세팅
            for i, component in enumerate(list_covid19_national_issue):
                issue_written_date = component['wrt_dt']
                issue_nation_name = component['country_nm']
                issue_title = component['title']
                issue_article = component['txt_origin_cn']

                item_issue_written_date = QTableWidgetItem(issue_written_date)
                item_issue_written_date.setFont(self.font_content)
                item_issue_nation_name = QTableWidgetItem(issue_nation_name)
                item_issue_nation_name.setFont(self.font_content)
                item_issue_title = QTableWidgetItem(issue_title)
                item_issue_title.setFont(self.font_content)
                item_issue_title.setToolTip(issue_article)  # 기사 내용을 툴팁으로 지정

                # 컬럼 수만큼 반복
                for j in range(len(list_column_covid19_national_issue)):
                    self.table_api_covid19_national_issue.setItem(i + 1, j, item_issue_written_date)
                    self.table_api_covid19_national_issue.setItem(i + 1, j + 1, item_issue_nation_name)
                    self.table_api_covid19_national_issue.setItem(i + 1, j + 2, item_issue_title)

            # 레이아웃에 테이블 추가
            self.v_layout_api_covid19_national_issue.addWidget(self.table_api_covid19_national_issue)

            # 검색결과가 없을 때
            if not list_covid19_national_issue:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("알림")
                msg.setText('검색 결과가 없습니다')
                msg.exec_()
        except Exception as e:
            print('{set_table_api_covid19_national_issue} - ' + str(e))
