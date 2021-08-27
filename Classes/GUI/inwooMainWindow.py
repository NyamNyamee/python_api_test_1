import sys
import time
import datetime

from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Classes.Util.Logger import logger

from Classes.GUI.inwooMainWidget import InwooMainWidget

from Classes.CrawlingTest.Movie import MovieCrawler
from Classes.CrawlingTest.Music import MusicCrawler
from Classes.CrawlingTest.Weather import WeatherCrawler
from Classes.CrawlingTest.Covid19 import Covid19Crawler
from Classes.CrawlingTest.Game import GameCrawler
from Classes.CrawlingTest.Accident import AccidentCrawler
from Classes.CrawlingTest.Kakao import KakaoCrawler
from Classes.CrawlingTest.ChatBot import ChatBotCrawler
from Classes.CrawlingTest.Gyeonggi_Info import GyeonggiInfoCrawler


class InwooMainWindow(QMainWindow):
    """ Inwoo App Main Window """

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """ 생성자 """
        try:
            # 아이콘 생성
            self.icon_exit_01 = QIcon('../resources/image/logout_01.png')
            self.icon_api_01 = QIcon('../resources/image/api_01.png')
            self.icon_movie_01 = QIcon('../resources/image/movie_01.png')
            self.icon_music_01 = QIcon('../resources/image/music_01.png')
            self.icon_weather_01 = QIcon('../resources/image/lightMode_01.png')
            self.icon_covid_01 = QIcon('../resources/image/coronaVirus_01.png')
            self.icon_game_01 = QIcon('../resources/image/esports_01.png')
            self.icon_accident_01 = QIcon('../resources/image/fire_01.png')
            self.icon_kakao_01 = QIcon('../resources/image/kakao_01.png')
            self.icon_chatbot_01 = QIcon('../resources/image/chat_01.png')
            self.icon_gyeonggi_01 = QIcon('../resources/image/place_01.png')

            # 윈도우 기본설정
            self.setWindowTitle('Inwoo\'s application')  # 윈도우 타이틀
            self.setWindowIcon(self.icon_api_01)  # 윈도우 아이콘 지정
            self.resize(1800, 800)  # 윈도우 너비, 높이 조절(픽셀)
            self.set_window_center()  # 윈도우를 화면 가운데로

            # 메뉴바
            self.set_window_menu_bar()

            # 툴바
            self.set_window_tool_bar()

            # 하단 상태표시줄
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')  # 현재시간을 문자열로 저장
            bottom_status_bar = self.statusBar()  # 상태표시줄 생성
            # bottom_status_bar.showMessage('오늘 날짜: ' + current_time)  # 메시지 설정
            self.setStatusTip('Now: ' + current_time)  # 윈도우에 마우스오버하면 하단 상태표시줄 메시지 표시

            # 메인위젯 지정
            self.inwoo_main_widget = InwooMainWidget()
            self.setCentralWidget(self.inwoo_main_widget)

            # 화면 띄우기
            self.show()  # 화면에 띄움
        except Exception as e:
            print('{init_ui} - ' + str(e))

    def set_window_center(self):
        """ 윈도우를 화면 가운대로 이동 """
        try:
            qr = self.frameGeometry()  # 윈도우 크기, 위치 파악해서 qr에 저장
            cp = QDesktopWidget().availableGeometry().center()  # 화면 크기, 위치 파악해서 cp에 저장
            qr.moveCenter(cp)  # 화면 중앙으로 윈도우 이동
            self.move(qr.topLeft())  # qr의 위치로 현재 윈도우 이동
        except Exception as e:
            print('{set_window_center} - ' + str(e))

    def set_window_menu_bar(self):
        """ 상단 메뉴바 설정 """
        try:
            # 상단 메뉴바
            menu_bar_top = self.menuBar()  # 메뉴바 생성
            menu_bar_top.setNativeMenuBar(False)
            # 상단 메뉴바에 메뉴 추가
            menu_bar_top_menu = menu_bar_top.addMenu('&Menu')

            # api 실행 액션
            action_set_public_api = QAction(self.icon_api_01, 'API', self)  # api 액션(아이콘, 텍스트, 붙일 윈도우)
            action_set_public_api.setShortcut('Ctrl+A')  # 단축키 설정
            action_set_public_api.setStatusTip('Public API Info')  # 하단 상태표시줄 문구 설정
            action_set_public_api.triggered.connect(self.set_window_toolbar_api)  # 클릭 시 set_window_toolbar_api() 실행

            # 종료 액션
            action_exit = QAction(self.icon_exit_01, 'Exit', self)  # 종료 액션(아이콘, 텍스트, 붙일 윈도우)
            action_exit.setShortcut('Ctrl+Q')  # 단축키 설정
            action_exit.setStatusTip('Exit Application')  # 하단 상태표시줄 문구 설정
            action_exit.triggered.connect(QCoreApplication.instance().quit)  # 클릭 시 종료

            # 상단 메뉴바 메뉴에 액션 추가
            menu_bar_top_menu.addAction(action_set_public_api)  # api 액션 추가
            menu_bar_top_menu.addAction(action_exit)  # 종료 액션 추가
        except Exception as e:
            print('{set_window_menu_bar} - ' + str(e))

    def set_window_tool_bar(self):
        """ 상단 툴바 설정 """
        try:
            self.tool_bar_main = QToolBar('main_tool_bar')  # 툴바 생성
            self.addToolBar(self.tool_bar_main)  # 윈도우에 툴바 지정
            self.tool_bar_main.setVisible(False)  # 일단 숨김
        except Exception as e:
            print('{set_window_tool_bar} - ' + str(e))

    def set_window_toolbar_api(self):
        """ 메뉴바 api 메뉴 선택 핸들러 """
        try:
            # 툴바 메뉴 전부 제거
            self.tool_bar_main.clear()
            
            # 영화 액션
            action_set_public_api_movie = QAction(self.icon_movie_01, 'Movie', self)  # 영화 액션(아이콘, 텍스트, 붙일 윈도우)
            action_set_public_api_movie.setToolTip('Movie')
            action_set_public_api_movie.setStatusTip('Movie')  # 하단 상태표시줄 문구 설정
            action_set_public_api_movie.triggered.connect(self.set_window_widget_api_movie)  # 클릭 시 set_window_widget_api_movie() 실행

            # 음악 액션
            action_set_public_api_music = QAction(self.icon_music_01, 'Music', self)  # 음악 액션(아이콘, 텍스트, 붙일 윈도우)
            action_set_public_api_music.setToolTip('Music')
            action_set_public_api_music.setStatusTip('Music')  # 하단 상태표시줄 문구 설정
            action_set_public_api_music.triggered.connect(self.set_window_widget_api_music)  # 클릭 시 set_window_widget_api_music() 실행

            # 날씨 액션
            action_set_public_api_weather = QAction(self.icon_weather_01, 'Weather', self)  # 날씨 액션(아이콘, 텍스트, 붙일 윈도우)
            action_set_public_api_weather.setToolTip('Weather')
            action_set_public_api_weather.setStatusTip('Weather')  # 하단 상태표시줄 문구 설정
            action_set_public_api_weather.triggered.connect(self.set_window_widget_api_music)  # 클릭 시 set_window_widget_api_music() 실행

            # 코로나 액션
            action_set_public_api_covid = QAction(self.icon_covid_01, 'Covid', self)  # 코로나 액션(아이콘, 텍스트, 붙일 윈도우)
            action_set_public_api_covid.setToolTip('Covid')
            action_set_public_api_covid.setStatusTip('Covid')  # 하단 상태표시줄 문구 설정
            action_set_public_api_covid.triggered.connect(self.set_window_widget_api_music)  # 클릭 시 set_window_widget_api_music() 실행

            # 게임 액션
            action_set_public_api_game = QAction(self.icon_game_01, 'Game', self)  # 게임 액션(아이콘, 텍스트, 붙일 윈도우)
            action_set_public_api_game.setToolTip('Game')
            action_set_public_api_game.setStatusTip('Game')  # 하단 상태표시줄 문구 설정
            action_set_public_api_game.triggered.connect(self.set_window_widget_api_music)  # 클릭 시 set_window_widget_api_music() 실행

            # 사고 액션
            action_set_public_api_accident = QAction(self.icon_accident_01, 'Accident', self)  # 사고 액션(아이콘, 텍스트, 붙일 윈도우)
            action_set_public_api_accident.setToolTip('Accident')
            action_set_public_api_accident.setStatusTip('Accident')  # 하단 상태표시줄 문구 설정
            action_set_public_api_accident.triggered.connect(self.set_window_widget_api_music)  # 클릭 시 set_window_widget_api_music() 실행

            # 카카오 액션
            action_set_public_api_kakao = QAction(self.icon_kakao_01, 'Kakao', self)  # 카카오 액션(아이콘, 텍스트, 붙일 윈도우)
            action_set_public_api_kakao.setToolTip('Kakao')
            action_set_public_api_kakao.setStatusTip('Kakao')  # 하단 상태표시줄 문구 설정
            action_set_public_api_kakao.triggered.connect(self.set_window_widget_api_music)  # 클릭 시 set_window_widget_api_music() 실행

            # 챗봇 액션
            action_set_public_api_chatbot = QAction(self.icon_chatbot_01, 'Chatbot', self)  # 챗봇 액션(아이콘, 텍스트, 붙일 윈도우)
            action_set_public_api_chatbot.setToolTip('Chatbot')
            action_set_public_api_chatbot.setStatusTip('Chatbot')  # 하단 상태표시줄 문구 설정
            action_set_public_api_chatbot.triggered.connect(self.set_window_widget_api_music)  # 클릭 시 set_window_widget_api_music() 실행

            # 경기도 액션
            action_set_public_api_gyeonggi = QAction(self.icon_gyeonggi_01, 'Gyeonggi', self)  # 경기도 액션(아이콘, 텍스트, 붙일 윈도우)
            action_set_public_api_gyeonggi.setToolTip('Gyeonggi')
            action_set_public_api_gyeonggi.setStatusTip('Gyeonggi')  # 하단 상태표시줄 문구 설정
            action_set_public_api_gyeonggi.triggered.connect(self.set_window_widget_api_music)  # 클릭 시 set_window_widget_api_music() 실행

            # api 툴바에 액션 추가
            self.tool_bar_main.addAction(action_set_public_api_movie)
            self.tool_bar_main.addAction(action_set_public_api_music)
            self.tool_bar_main.addAction(action_set_public_api_weather)
            self.tool_bar_main.addAction(action_set_public_api_covid)
            self.tool_bar_main.addAction(action_set_public_api_game)
            self.tool_bar_main.addAction(action_set_public_api_accident)
            self.tool_bar_main.addAction(action_set_public_api_kakao)
            self.tool_bar_main.addAction(action_set_public_api_chatbot)
            self.tool_bar_main.addAction(action_set_public_api_gyeonggi)

            # 툴바 노출
            self.tool_bar_main.setVisible(True)
        except Exception as e:
            print('{set_window_toolbar_api} - ' + str(e))

    def set_window_widget_api_movie(self):
        """ api 툴바 영화 메뉴 선택 핸들러 """
        try:
            self.inwoo_main_widget.set_tabs_movie()
        except Exception as e:
            print('{set_window_widget_api_movie} - ' + str(e))

    def set_window_widget_api_music(self):
        """ api 툴바 음악 메뉴 선택 핸들러 """
        try:
            print('music')
        except Exception as e:
            print('{set_window_widget_api_music} - ' + str(e))

