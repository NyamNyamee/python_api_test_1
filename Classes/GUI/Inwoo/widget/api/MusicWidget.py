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


class MusicWidget(QWidget):
    """ inwoo app music widget """

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

            # 오늘날짜
            self.date_today = QDate().currentDate()

            # 폰트
            self.font_header = QFont()  # 헤더용 폰트 객체 생성
            self.font_header.setBold(True)  # 굵게
            self.font_header.setPointSize(8)  # 글자 포인트

            self.font_content = QFont()  # 내용물 폰트 객체 생성
            self.font_content.setPointSize(8)  # 글자 포인트

            # 음악 수직 레이아웃 생성
            self.v_layout_music = QVBoxLayout()
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
        """ 대출일 날짜 변경 시 이벤트 핸들러 """
        try:
            # 각 날짜 값 저장
            selected_date_picker_01 = self.date_picker_01.date()
            selected_date_picker_02 = self.date_picker_02.date()

            self.date_picker_01.setMaximumDate(selected_date_picker_02)  # 시작 대출일 최대치를 끝 대출일 선택값으로
            self.date_picker_02.setMinimumDate(selected_date_picker_01)  # 끝 대출일 최소치를 시작 대출일 선택값으로
        except Exception as e:
            print('{date_picker_handler} - ' + str(e))

    def set_tabs_music(self):
        """ 음악 메뉴 탭 생성 """
        try:
            # 메인 위젯의 레이아웃을 음악 수직 레이아웃으로 지정
            self.setLayout(self.v_layout_music)

            # music_tabs 라는 이름의 QTabWidget이 있다면
            if self.findChild(QTabWidget, 'music_tabs'):
                self.layout().removeWidget(self.tabs_api_music)  # 음악 탭 제거

            # 탭 생성
            self.tabs_api_music = QTabWidget()
            self.tabs_api_music.setObjectName('music_tabs')

            # FLO 음악 최신 100곡
            self.set_form_api_music_flo_new_100()

            # 음악 수직 레이아웃에 음악 탭 추가
            self.v_layout_music.addWidget(self.tabs_api_music)
        except Exception as e:
            print('{set_tabs_music} - ' + str(e))


    def set_form_api_music_flo_new_100(self):
        """ API music FLO new 100 테이블 폼 세팅 """
        try:
            # 수직 레이아웃 생성
            self.v_layout_api_music_flo_new_100 = QVBoxLayout()

            # 국내 해외 선택 입력란
            self.combo_api_music_flo_new_100 = QComboBox()
            self.combo_api_music_flo_new_100.addItem('국내')
            self.combo_api_music_flo_new_100.addItem('해외')

            # 검색 버튼
            btn_api_music_flo_new_100_run = QPushButton('검색')
            btn_api_music_flo_new_100_run.resize(btn_api_music_flo_new_100_run.sizeHint())
            btn_api_music_flo_new_100_run.clicked.connect(self.set_table_api_music_flo_new_100)

            # 수직 레아이웃에 위젯 추가
            self.v_layout_api_music_flo_new_100.addWidget(self.combo_api_music_flo_new_100)
            self.v_layout_api_music_flo_new_100.addWidget(btn_api_music_flo_new_100_run)
            self.v_layout_api_music_flo_new_100.addSpacing(700)

            # 그룹박스 생성
            group_box_api_music_flo_new_100 = QGroupBox('지역 선택')

            # 그룹박스의 레이아웃을 수직 레이아웃으로
            group_box_api_music_flo_new_100.setLayout(self.v_layout_api_music_flo_new_100)

            # 탭에 그룹박스 추가
            self.tabs_api_music.addTab(group_box_api_music_flo_new_100, 'FLO 최신 100곡')
        except Exception as e:
            print('{set_form_api_music_flo_new_100} - ' + str(e))


    def set_table_api_music_flo_new_100(self):
        """ API music FLO new 100 테이블 데이터 세팅 """
        try:
            if self.v_layout_api_music_flo_new_100.count() > 3:
                self.v_layout_api_music_flo_new_100.removeWidget(self.table_api_music_flo_new_100)
            else:
                self.v_layout_api_music_flo_new_100.addSpacing(-700)

            # 테이블 컬럼 리스트
            list_column_flo_new_100 = ['번호', '곡명', '아티스트', '발매일', '장르', '앨범', '커버']

            # 국내외 선택 콤보박스 값
            selected_location = 'KPOP' if self.combo_api_music_flo_new_100.currentText() == '국내' else 'POP'

            # 요청 정보
            host = 'https://www.music-flo.com'
            path = '/api/meta/v1/track/{0}/new'.format(selected_location)
            headers = None
            query = '?page=1&size=100'
            method = 'GET'
            data = None

            # 응답
            try:
                res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)
            except Exception as e:
                raise RuntimeError("[FLO] 최신 100곡 요청 실패: " + str(e))

            # 응답의 바디를 json형태로 파싱
            parsed_object = json.loads(res.text)

            # 필요 데이터만 가져옴
            list_music_flo_new_100 = parsed_object['data']['list']

            # 테이블 생성
            self.table_api_music_flo_new_100 = QTableWidget(len(list_music_flo_new_100) + 1, len(list_column_flo_new_100), self)
            self.table_api_music_flo_new_100.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.table_api_music_flo_new_100.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.table_api_music_flo_new_100.horizontalHeader().setVisible(False)
            self.table_api_music_flo_new_100.verticalHeader().setVisible(False)

            # 컬럼 세팅
            for i, component in enumerate(list_column_flo_new_100):
                item_column_flo_new_100 = QTableWidgetItem(component)
                item_column_flo_new_100.setFont(self.font_header)
                item_column_flo_new_100.setBackground(QColor(200, 200, 200))
                item_column_flo_new_100.setTextAlignment(Qt.AlignCenter)
                self.table_api_music_flo_new_100.setItem(0, i, item_column_flo_new_100)

            # 데이터 세팅
            for i, component in enumerate(list_music_flo_new_100):
                music_name = component['name']
                music_album_title = component['album']['title']
                music_album_release_date = component['album']['releaseYmd']
                music_album_genre = component['album']['genreStyle']
                music_artist = component['representationArtist']['name']
                music_album_image_url = component['album']['imgList'][0]['url']
                music_album_image = urllib.request.urlopen(music_album_image_url).read()
                pixmap = QPixmap()
                pixmap.loadFromData(music_album_image)
                pixmap.scaled(500, 500)
                self.label = QLabel()
                # self.label.resize(1000, 1000)
                self.label.setPixmap(pixmap)

                item_music_num = QTableWidgetItem(str(i + 1))
                item_music_num.setFont(self.font_content)
                item_music_name = QTableWidgetItem(music_name)
                item_music_name.setFont(self.font_content)
                item_music_album_title = QTableWidgetItem(music_album_title)
                item_music_album_title.setFont(self.font_content)
                item_music_album_release_date = QTableWidgetItem(music_album_release_date)
                item_music_album_release_date.setFont(self.font_content)
                item_music_album_genre = QTableWidgetItem(music_album_genre)
                item_music_album_genre.setFont(self.font_content)
                item_music_artist = QTableWidgetItem(music_artist)
                item_music_artist.setFont(self.font_content)

                # 컬럼 수만큼 반복
                for j in range(len(list_column_flo_new_100)):
                    self.table_api_music_flo_new_100.setItem(i + 1, j, item_music_num)
                    self.table_api_music_flo_new_100.setItem(i + 1, j + 1, item_music_name)
                    self.table_api_music_flo_new_100.setItem(i + 1, j + 2, item_music_artist)
                    self.table_api_music_flo_new_100.setItem(i + 1, j + 3, item_music_album_release_date)
                    self.table_api_music_flo_new_100.setItem(i + 1, j + 4, item_music_album_genre)
                    self.table_api_music_flo_new_100.setItem(i + 1, j + 5, item_music_album_title)
                    self.table_api_music_flo_new_100.setCellWidget(i + 1, j + 6, self.label)  # 셀에 위젯 지정
                    self.table_api_music_flo_new_100.setRowHeight(i + 1, 80)  # 셀 높이 조정(행, 높이 픽셀)

            # 레이아웃에 테이블 추가
            self.v_layout_api_music_flo_new_100.addWidget(self.table_api_music_flo_new_100)
        except Exception as e:
            print('{set_table_api_music_flo_new_100} - ' + str(e))
