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


class GameWidget(QWidget):
    """ inwoo app game widget """

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

            # 키
            # Steam
            self.steam_key = self.property_reader.get('STEAM_KEY').data
            # Blizzard
            self.blizzard_client_name = self.property_reader.get('BLIZZARD_CLIENT_NAME').data
            self.blizzard_client_id = self.property_reader.get('BLIZZARD_CLIENT_ID').data
            self.blizzard_client_secret = self.property_reader.get('BLIZZARD_CLIENT_SECRET').data
            self.blizzard_redirect_url = self.property_reader.get('BLIZZARD_REDIRECT_URL').data
            self.blizzard_region = self.property_reader.get('BLIZZARD_REGION').data
            self.blizzard_locale = self.property_reader.get('BLIZZARD_LOCALE').data
            self.blizzard_locale = self.property_reader.get('BLIZZARD_LOCALE').data

            # 오늘날짜
            self.date_today = QDate().currentDate()

            # 폰트
            self.font_header = QFont()  # 헤더용 폰트 객체 생성
            self.font_header.setBold(True)  # 굵게
            self.font_header.setPointSize(8)  # 글자 포인트

            self.font_content = QFont()  # 내용물 폰트 객체 생성
            self.font_content.setPointSize(8)  # 글자 포인트

            # 게임 수직 레이아웃 생성
            self.v_layout_game = QVBoxLayout()
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

    def set_tabs_game(self):
        """ 게임 메뉴 탭 생성 """
        try:
            # 메인 위젯의 레이아웃을 게임 수직 레이아웃으로 지정
            self.setLayout(self.v_layout_game)

            # game_tabs 라는 이름의 QTabWidget이 있다면
            if self.findChild(QTabWidget, 'game_tabs'):
                self.layout().removeWidget(self.tabs_api_game)  # 게임 탭 제거

            # 탭 생성
            self.tabs_api_game = QTabWidget()
            self.tabs_api_game.setObjectName('game_tabs')

            # Steam 테이블 폼 세팅
            self.set_form_api_game_steam()

            # Blizzard 테이블 폼 세팅
            self.set_form_api_game_blizzard()

            # 게임 수직 레이아웃에 게임 탭 추가
            self.v_layout_game.addWidget(self.tabs_api_game)
        except Exception as e:
            print('{set_tabs_game} - ' + str(e))


    def set_form_api_game_steam(self):
        """ API game Steam 테이블 폼 세팅 """
        try:
            # 수직 레이아웃 생성
            self.v_layout_api_game_steam = QVBoxLayout()

            # steam 게임 메뉴 선택 콤보박스
            self.combo_api_game_steam = QComboBox()
            self.combo_api_game_steam.addItem('선택')
            self.combo_api_game_steam.addItem('게임조회')
            self.combo_api_game_steam.currentIndexChanged.connect(self.set_form_api_game_steam_menu)  # 옵션 변경 이벤트 핸들러

            # steam 게임조회 입력란
            self.line_edit_api_game_steam_game_info = QLineEdit()
            self.line_edit_api_game_steam_game_info.setPlaceholderText('검색할 게임을 입력해 주세요(영문 소문자)')

            # 검색 버튼
            self.btn_api_api_game_steam_run = QPushButton('검색')
            self.btn_api_api_game_steam_run.resize(self.btn_api_api_game_steam_run.sizeHint())
            self.btn_api_api_game_steam_run.clicked.connect(self.set_table_api_game_steam)

            # 수직 레아이웃에 위젯 추가
            self.v_layout_api_game_steam.addWidget(self.combo_api_game_steam)
            # self.v_layout_api_game_steam.addWidget(btn_api_api_game_steam_run)
            self.v_layout_api_game_steam.addSpacing(700)

            # 그룹박스 생성
            group_box_api_game_steam = QGroupBox('메뉴 선택')
            # 그룹박스의 레이아웃을 수직 레이아웃으로
            group_box_api_game_steam.setLayout(self.v_layout_api_game_steam)

            # 탭에 그룹박스 추가
            self.tabs_api_game.addTab(group_box_api_game_steam, 'Steam')
        except Exception as e:
            print('{set_form_api_game_steam} - ' + str(e))

    def set_form_api_game_steam_menu(self):
        """ steam - 메뉴 옵션 변경 이벤트 핸들러 """
        try:
            selected_menu_index = self.combo_api_game_steam.currentIndex()
            if selected_menu_index == 0:  # 선택
                self.line_edit_api_game_steam_game_info.setParent(None)  # 해당 위젯의 부모(레이아웃)의 아이템을 비움?
                self.btn_api_api_game_steam_run.setParent(None)
                if self.findChild(QTableWidget, 'table_steam'):  # 해당 이름의 위젯 발견 시
                    self.table_api_game_steam.setParent(None)
                    self.v_layout_api_game_steam.addSpacing(700)
            elif selected_menu_index == 1:  # steam 게임 조회
                self.v_layout_api_game_steam.addSpacing(-700)  # 여백 제거
                self.v_layout_api_game_steam.addWidget(self.line_edit_api_game_steam_game_info)
                self.v_layout_api_game_steam.addWidget(self.btn_api_api_game_steam_run)
                self.v_layout_api_game_steam.addSpacing(700)  # 다시 여백 추가

        except Exception as e:
            print('{set_form_api_game_steam_menu} - ' + str(e))

    def set_table_api_game_steam(self):
        """ API game 스팀 테이블 데이터 세팅 """
        try:
            # 선택한 steam 메뉴
            selected_menu_index = self.combo_api_game_steam.currentIndex()
            if selected_menu_index == 1:  # 게임조회
                if self.findChild(QTableWidget, 'table_steam'):  # 해당 이름의 위젯 발견 시
                    self.v_layout_api_game_steam.removeWidget(self.table_api_game_steam)
                else:
                    self.v_layout_api_game_steam.addSpacing(-700)

                # 테이블 컬럼 리스트
                list_column_game_steam_game_info = ['고유번호', '게임명']

                # 게임 입력 값
                searched_game_value = str(self.line_edit_api_game_steam_game_info.text().strip())

                # 요청 정보
                host = 'https://api.steampowered.com'
                path = '/ISteamApps/GetAppList/v1/'
                headers = None
                query = ''
                method = 'GET'
                data = None

                # 응답
                try:
                    res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)
                except Exception as e:
                    raise RuntimeError("[Steam] 게임 정보 요청 실패: " + str(e))

                # 응답의 바디를 json형태로 파싱
                parsed_object = json.loads(res.text)

                # 필요 데이터만 가져옴
                list_game_steam_game_info = parsed_object['applist']['apps']['app']

                # 검색 결과가 포함된 결과 개수
                result_count = 0

                # 검색 결과가 포함된 결과 개수 조회
                for i, component in enumerate(list_game_steam_game_info):
                    steam_game_name = component['name']
                    if searched_game_value in steam_game_name:
                        result_count += 1

                # 테이블 생성
                self.table_api_game_steam = QTableWidget(result_count + 1, len(list_column_game_steam_game_info), self)
                self.table_api_game_steam.setObjectName('table_steam')
                self.table_api_game_steam.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.table_api_game_steam.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.table_api_game_steam.horizontalHeader().setVisible(False)
                self.table_api_game_steam.verticalHeader().setVisible(False)

                # 컬럼 세팅
                for i, component in enumerate(list_column_game_steam_game_info):
                    item_column_game_steam = QTableWidgetItem(component)
                    item_column_game_steam.setFont(self.font_header)
                    item_column_game_steam.setBackground(QColor(200, 200, 200))
                    item_column_game_steam.setTextAlignment(Qt.AlignCenter)
                    self.table_api_game_steam.setItem(0, i, item_column_game_steam)

                # 데이터를 입력하 테이블 행번호로 사용하기 위해 다시 0으로 초기화
                result_count = 0

                # 데이터 세팅
                for i, component in enumerate(list_game_steam_game_info):
                    steam_game_id = str(component['appid'])
                    steam_game_name = component['name']

                    if searched_game_value in steam_game_name:
                        item_steam_game_id = QTableWidgetItem(steam_game_id)
                        item_steam_game_id.setFont(self.font_content)
                        item_steam_game_name = QTableWidgetItem(steam_game_name)
                        item_steam_game_name.setFont(self.font_content)

                        result_count += 1

                        # 컬럼 수만큼 반복
                        for j in range(len(list_column_game_steam_game_info)):
                            self.table_api_game_steam.setItem(result_count, j, item_steam_game_id)
                            self.table_api_game_steam.setItem(result_count, j + 1, item_steam_game_name)
                    else:
                        continue

                # 레이아웃에 테이블 추가
                self.v_layout_api_game_steam.addWidget(self.table_api_game_steam)

                # 검색결과가 없을 때
                if not result_count:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle("알림")
                    msg.setText('검색 결과가 없습니다')
                    msg.exec_()
        except Exception as e:
            print('{set_table_api_game_steam} - ' + str(e))

    def set_form_api_game_blizzard(self):
        """ API game blizzard 테이블 폼 세팅 """
        try:
            # 수직 레이아웃 생성
            self.v_layout_api_game_blizzard = QVBoxLayout()

            # blizzard 게임 메뉴 선택 콤보박스
            self.combo_api_game_blizzard = QComboBox()
            self.combo_api_game_blizzard.addItem('선택')
            self.combo_api_game_blizzard.addItem('Diablo3')
            self.combo_api_game_blizzard.addItem('Starcraft2')
            self.combo_api_game_blizzard.addItem('HearthStone')
            self.combo_api_game_blizzard.addItem('WOW')
            self.combo_api_game_blizzard.addItem('WOW Classic')
            self.combo_api_game_blizzard.currentIndexChanged.connect(self.set_form_api_game_blizzard_menu)  # 옵션 변경 이벤트 핸들러

            # blizzard diablo3 메뉴 선택 콤보박스
            self.combo_api_game_blizzard_diablo3 = QComboBox()
            self.combo_api_game_blizzard_diablo3.addItem('선택')
            self.combo_api_game_blizzard_diablo3.addItem('유저 검색')
            self.combo_api_game_blizzard_diablo3.currentIndexChanged.connect(self.set_form_api_game_blizzard_diablo3_menu)  # 옵션 변경 이벤트 핸들러

            # blizzard 입력란
            self.line_edit_api_game_blizzard = QLineEdit()
            self.line_edit_api_game_blizzard.setPlaceholderText('배틀태그를 입력해 주세요')

            # 검색 버튼
            self.btn_api_api_game_blizzard_run = QPushButton('검색')
            self.btn_api_api_game_blizzard_run.resize(self.btn_api_api_game_blizzard_run.sizeHint())
            self.btn_api_api_game_blizzard_run.clicked.connect(self.set_table_api_game_blizzard)

            # 수직 레아이웃에 위젯 추가
            self.v_layout_api_game_blizzard.addWidget(self.combo_api_game_blizzard)
            self.v_layout_api_game_blizzard.addSpacing(700)

            # 그룹박스 생성
            group_box_api_game_blizzard = QGroupBox('메뉴 선택')
            # 그룹박스의 레이아웃을 수직 레이아웃으로
            group_box_api_game_blizzard.setLayout(self.v_layout_api_game_blizzard)

            # 탭에 그룹박스 추가
            self.tabs_api_game.addTab(group_box_api_game_blizzard, 'Blizzard')
        except Exception as e:
            print('{set_form_api_game_blizzard} - ' + str(e))

    def set_form_api_game_blizzard_menu(self):
        """ blizzard - 메뉴 옵션 변경 이벤트 핸들러 """
        try:
            selected_menu_index = self.combo_api_game_blizzard.currentIndex()
            if selected_menu_index == 0:  # 선택
                self.combo_api_game_blizzard_diablo3.setParent(None)  # 해당 위젯의 부모(레이아웃)의 아이템을 비움?
                self.line_edit_api_game_blizzard.setParent(None)
                self.btn_api_api_game_blizzard_run.setParent(None)
                if self.findChild(QTableWidget, 'table_blizzard'):  # 해당 이름의 위젯 발견 시
                    self.table_api_game_blizzard.setParent(None)
                    self.v_layout_api_game_blizzard.addSpacing(700)
            elif selected_menu_index == 1:  # Diablo3
                self.v_layout_api_game_blizzard.addSpacing(-700)  # 여백 제거
                self.v_layout_api_game_blizzard.addWidget(self.combo_api_game_blizzard_diablo3)
                self.v_layout_api_game_blizzard.addSpacing(700)  # 다시 여백 추가

        except Exception as e:
            print('{set_form_api_game_blizzard_menu} - ' + str(e))

    def set_form_api_game_blizzard_diablo3_menu(self):
        """ blizzard - diablo3 메뉴 옵션 변경 이벤트 핸들러 """
        try:
            selected_menu_index = self.combo_api_game_blizzard_diablo3.currentIndex()
            if selected_menu_index == 0:  # 선택
                self.line_edit_api_game_blizzard.setParent(None)  # 해당 위젯의 부모(레이아웃)의 아이템을 비움?
                self.btn_api_api_game_blizzard_run.setParent(None)  # 해당 위젯의 부모(레이아웃)의 아이템을 비움?
                if self.findChild(QTableWidget, 'table_blizzard'):  # 해당 이름의 위젯 발견 시
                    self.table_api_game_blizzard.setParent(None)
                    self.v_layout_api_game_blizzard.addSpacing(700)
            elif selected_menu_index == 1:  # Diablo3
                self.v_layout_api_game_blizzard.addSpacing(-700)  # 여백 제거
                self.v_layout_api_game_blizzard.addWidget(self.line_edit_api_game_blizzard)
                self.v_layout_api_game_blizzard.addWidget(self.btn_api_api_game_blizzard_run)
                self.v_layout_api_game_blizzard.addSpacing(700)  # 다시 여백 추가

        except Exception as e:
            print('{set_form_api_game_blizzard_diablo3_menu} - ' + str(e))


    def set_table_api_game_blizzard(self):
        """ API game blizzard 테이블 데이터 세팅 """
        try:
            selected_blizzard_menu_index = self.combo_api_game_blizzard.currentIndex()
            selected_blizzard_diablo3_menu_index = self.combo_api_game_blizzard_diablo3.currentIndex()

            if selected_blizzard_menu_index == 1:  # diablo3 선택 시
                try:
                    # 요청 정보
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
                    res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers,
                                                                       query=query,
                                                                       method=method, data=data)

                    # json형태의 문자열 바디를 딕셔너리로 파싱
                    parsed_object = json.loads(res.text)
                    
                    # 필요 데이터 추출
                    blizzard_access_token = parsed_object['access_token']

                    # 멤버변수에 토큰, 리프레쉬토큰 값 지정
                    self.blizzard_access_token = blizzard_access_token
                except Exception as e:
                    raise RuntimeError("[Blizzard] 토큰 요청 실패: " + str(e))
            if selected_blizzard_diablo3_menu_index == 1:  # diablo3_프로필조회 선택 시
                if self.findChild(QTableWidget, 'table_blizzard'):  # 해당 이름의 위젯 발견 시 
                    self.layout().removeWidget(self.table_api_game_blizzard)  # 위젯 제거
                else:
                    self.v_layout_api_game_blizzard.addSpacing(-700)

                # 테이블 컬럼 리스트
                list_column_game_blizzard_diablo3_profile = ['정복자레벨', '길드명', '몬스터처치(일반/엘리트/하드코어)', '케릭터명', '클래스', '레벨']

                # 검색 값 저장
                searched_text_value = str(self.line_edit_api_game_blizzard.text().strip().replace('#', '%23'))

                # 요청 정보
                host = 'https://' + self.blizzard_region + '.api.blizzard.com'
                path = '/d3/profile/{0}/'.format(searched_text_value)
                headers = {'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8'}
                query = '?locale={0}&access_token={1}'.format(self.blizzard_locale, self.blizzard_access_token)
                method = 'GET'
                data = None

                # 응답
                try:
                    res = TransmitterReceiver.get_response_for_request(host=host, path=path, headers=headers, query=query, method=method, data=data)
                except Exception as e:
                    raise RuntimeError("[Blizzard] Diablo3 프로필 요청 실패: " + str(e))

                # 응답 실패일 때
                if res.status_code != 200:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle("알림")
                    msg.setText('검색 결과가 없습니다')
                    msg.exec_()
                    self.v_layout_api_game_blizzard.addSpacing(700)
                    return

                # 응답의 바디를 json형태로 파싱
                parsed_object = json.loads(res.text)

                # 필요 데이터만 가져옴
                paragon_level = str(parsed_object['paragonLevel'])
                guild_name = 'None' if parsed_object['guildName'] == '' else parsed_object['guildName']
                kills_monsters = str(parsed_object['kills']['monsters'])
                kills_elites = str(parsed_object['kills']['elites'])
                kills_hardcore_monsters = str(parsed_object['kills']['hardcoreMonsters'])
                kills_total = kills_monsters + '/' + kills_elites + '/' + kills_hardcore_monsters
                heroes = parsed_object['heroes']

                # 테이블 생성
                self.table_api_game_blizzard = QTableWidget(len(heroes) + 1, len(list_column_game_blizzard_diablo3_profile), self)
                self.table_api_game_blizzard.setObjectName('table_blizzard')
                self.table_api_game_blizzard.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.table_api_game_blizzard.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.table_api_game_blizzard.horizontalHeader().setVisible(False)
                self.table_api_game_blizzard.verticalHeader().setVisible(False)
                self.table_api_game_blizzard.setSpan(1, 0, len(heroes), 1)  # (1, 0)셀을 영웅수x1만큼 병합
                self.table_api_game_blizzard.setSpan(1, 1, len(heroes), 1)  # (1, 1)셀을 영웅수x1만큼 병합
                self.table_api_game_blizzard.setSpan(1, 2, len(heroes), 1)  # (1, 2)셀을 영웅수x1만큼 병합

                # 컬럼 세팅
                for i, component in enumerate(list_column_game_blizzard_diablo3_profile):
                    item_column_game_blizzard_diablo3_profile = QTableWidgetItem(component)
                    item_column_game_blizzard_diablo3_profile.setFont(self.font_header)
                    item_column_game_blizzard_diablo3_profile.setBackground(QColor(200, 200, 200))
                    item_column_game_blizzard_diablo3_profile.setTextAlignment(Qt.AlignCenter)
                    self.table_api_game_blizzard.setItem(0, i, item_column_game_blizzard_diablo3_profile)

                # 데이터 세팅
                for i, component in enumerate(heroes):
                    item_paragon_level = QTableWidgetItem(paragon_level)
                    item_paragon_level.setFont(self.font_content)
                    item_guild_name = QTableWidgetItem(guild_name)
                    item_guild_name.setFont(self.font_content)
                    item_kills_total = QTableWidgetItem(kills_total)
                    item_kills_total.setFont(self.font_content)
                    item_heroes = QTableWidgetItem(str(heroes))
                    item_heroes.setFont(self.font_content)

                    hero_name = component['name']
                    hero_class = component['class']
                    hero_level = str(component['level'])

                    item_hero_name = QTableWidgetItem(hero_name)
                    item_hero_name.setFont(self.font_content)
                    item_hero_class = QTableWidgetItem(hero_class)
                    item_hero_class.setFont(self.font_content)
                    item_hero_level = QTableWidgetItem(hero_level)
                    item_hero_level.setFont(self.font_content)

                    # 컬럼 개수만큼 반복
                    self.table_api_game_blizzard.setItem(i + 1, 0, item_paragon_level)
                    self.table_api_game_blizzard.setItem(i + 1, 1, item_guild_name)
                    self.table_api_game_blizzard.setItem(i + 1, 2, item_kills_total)
                    self.table_api_game_blizzard.setItem(i + 1, 3, item_hero_name)
                    self.table_api_game_blizzard.setItem(i + 1, 4, item_hero_class)
                    self.table_api_game_blizzard.setItem(i + 1, 5, item_hero_level)

                # 레이아웃에 테이블 추가
                self.v_layout_api_game_blizzard.addWidget(self.table_api_game_blizzard)

                # 검색결과가 없을 때
                if not heroes:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle("알림")
                    msg.setText('검색 결과가 없습니다')
                    msg.exec_()
        except Exception as e:
            print('{set_table_api_game_blizzard} - ' + str(e))
