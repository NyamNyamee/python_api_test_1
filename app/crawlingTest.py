import sys
import time
import sentry_sdk as sentry
import jproperties

from Classes.Util.Logger import logger

from Classes.CrawlingTest.Movie import MovieCrawler
from Classes.CrawlingTest.Music import MusicCrawler
from Classes.CrawlingTest.Weather import WeatherCrawler
from Classes.CrawlingTest.Covid19 import Covid19Crawler
from Classes.CrawlingTest.Game import GameCrawler
from Classes.CrawlingTest.Accident import AccidentCrawler
from Classes.CrawlingTest.Kakao import KakaoCrawler
from Classes.CrawlingTest.ChatBot import ChatBotCrawler
from Classes.CrawlingTest.Gyeonggi_Info import GyeonggiInfoCrawler

""" ◀ 여러 api를 사용하는 데이터 크롤러 모듈 ▶ """
if __name__ == '__main__':
    property_reader = jproperties.Properties()
    info_message = None
    try:
        # with open('../resources/auth.properties', 'rb') as auth_properties:
        with open('..//resources/auth/auth.properties', 'rb') as auth_properties:
            property_reader.load(auth_properties)
    except Exception as e:
        info_message = '[에러] cannot open .properties file'
        logger.exception(f'{info_message}: {str(e)}')
        print(info_message)

    # Sentry Config
    sentry.init(
        # dsn=property_reader.get('SENTRY_DSN').data
        # ,debug=True
    )
    while True:
        try:
            main_menu_number = int(input('[알림] 원하는 메뉴를 입력해 주세요.\n0:프로그램종료 | 1:영화 | 2:음악 | 3:날씨 | 4:코로나19 | 5:게임 | 6:사고 | 7:카카오 | 8:챗봇 | 9:경기도정보\n'))
        except Exception as e:
            info_message = '[경고] 숫자만 입력해 주세요.\n'
            print(info_message)
            continue

        if main_menu_number == 0:
            """ 프로그램 종료 """
            break

        elif main_menu_number == 1:
            """ 영화정보 크롤링 """
            movie_crawler = MovieCrawler(kofic_key=property_reader.get('KOFIC_KEY').data)

            while True:
                try:
                    movie_menu_number = int(input('[알림] 원하는 메뉴를 입력해 주세요.\n0:메인메뉴 | 1:박스오피스검색 | 2:영화검색 | 3:영화인검색\n'))
                except Exception as e:
                    info_message = '[경고] 숫자만 입력해 주세요.\n'
                    print(info_message)
                    continue

                if movie_menu_number == 0:
                    """ 메인 메뉴로 이동 """
                    break

                elif movie_menu_number == 1:
                    """ 영화진흥위원회 박스오피스 조회 """
                    try:
                        target_date = input('[알림] 조회할 날짜를 입력하세요. ex)2021-04-05\n').replace('-', '').strip()
                        if len(target_date) != 8:
                            info_message = '[알림] 연월일을 yyyy-MM-dd 형태로 입력해 주세요.\n'
                            print(info_message)
                            continue
                        if int(target_date) > int(time.strftime('%Y%m%d')) - 1:
                            info_message = '[알림] 오늘 날짜 이상은 조회할 수 없습니다.\n'
                            print(info_message)
                            continue

                        movie_crawler.get_box_office_list_by_date(target_date=target_date)
                    except Exception as e:
                        logger.exception(f'[에러] 영화진흥위원회 박스오피스 조회: {str(e)}')
                        sentry.capture_exception(e)
                        print()
                        continue

                elif movie_menu_number == 2:
                    """ 영화진흥위원회 영화 목록, 상세정보 검색 """
                    movie_name = input('[알림] 검색할 영화제목을 입력하세요: ').strip()
                    try:
                        movie_crawler.get_movie_list_by_movie_name(movie_name=movie_name)
                    except Exception as e:
                        sentry.capture_exception(e)
                        logger.exception(f'[에러] 영화진흥위원회 영화목록, 상세정보 조회: {str(e)}')
                        print()
                        continue

                elif movie_menu_number == 3:
                    """ 영화진흥위원회 영화인 목록 검색 """
                    person_name = input('[알림] 검색할 영화인 이름을 입력하세요: ').strip()
                    try:
                        movie_crawler.get_movie_person_by_person_name(person_name=person_name)
                    except Exception as e:
                        sentry.capture_exception(e)
                        logger.exception(f'[에러] 영화진흥위원회 영화인 조회: {str(e)}')
                        print()
                        continue

                else:
                    info_message = '[알림] 메뉴 목록을 선택해 주세요.\n'
                    print(info_message)
                    continue

        elif main_menu_number == 2:
            """ 음악정보 크롤링 """
            music_crawler = MusicCrawler()

            while True:
                try:
                    music_menu_number = int(input('[알림] 원하는 메뉴를 입력해 주세요.\n0:메인메뉴 | 1:국내New100 | 2:해외New100\n'))
                except Exception as e:
                    info_message = '[경고] 숫자만 입력해 주세요.\n'
                    print(info_message)
                    continue

                try:
                    if music_menu_number == 0:
                        """ 메인 메뉴로 이동 """
                        break

                    elif music_menu_number == 1:
                        """ FLO 최신곡(국내) 조회 """
                        location = 'KPOP'
                        music_crawler.get_latest_song(location=location)

                    elif music_menu_number == 2:
                        """ FLO 최신곡(해외) 조회 """
                        location = 'POP'
                        music_crawler.get_latest_song(location=location)

                    else:
                        info_message = '[알림] 메뉴 목록을 선택해 주세요.\n'
                        print(info_message)
                        continue
                except Exception as e:
                    sentry.capture_exception(e)
                    logger.exception(f'[에러] FLO 최신곡 조회: {str(e)}')
                    print()
                    continue

        elif main_menu_number == 3:
            """ 날씨정보 크롤링 """
            weather_crawler = WeatherCrawler(data_gov_key=property_reader.get('DATA_GOV_KEY').data)

            while True:
                try:
                    weather_menu_number = int(input('[알림] 원하는 메뉴를 입력해 주세요.\n0:메인메뉴 | 1:지난 날씨정보 | 2:오늘 날씨정보\n'))
                except Exception as e:
                    info_message = '[경고] 숫자만 입력해 주세요.\n'
                    print(info_message)
                    continue

                if weather_menu_number == 0:
                    """ 메인 메뉴로 이동 """
                    break

                elif weather_menu_number == 1:
                    """ 공공데이터포털 지난 날씨정보 검색 """
                    start_date = input('[알림] 조회할 날짜를 입력하세요. ex)2021-04-05\n').replace('-', '').strip()

                    try:
                        end_date = int(start_date) + 1  # 조회 시작날짜 + 1
                    except Exception as e:
                        info_message = '[경고] 숫자만 입력해 주세요.\n'
                        print(info_message)
                        continue

                    if len(start_date) != 8:
                        info_message = '[알림] 연월일을 yyyy-MM-dd 형태로 입력해 주세요.\n'
                        print(info_message)
                        continue
                    if int(start_date) > int(time.strftime('%Y%m%d')) - 2:
                        info_message = '[알림] 어제 날씨 정보 조회 시, 그저께 날짜를 입력해 주세요.\n'
                        print(info_message)
                        continue
                    if int(start_date) < 19071001:
                        info_message = '[알림] 1907-10-01 이전 날짜는 조회할 수 없습니다.\n'
                        print(info_message)
                        continue

                    weather_location = 108  # 지점코드(서울 임시 고정)

                    try:
                        weather_crawler.get_ex_weather_info(start_date=start_date, end_date=end_date, weather_location=weather_location)
                    except Exception as e:
                        sentry.capture_exception(e)
                        logger.exception(f'[에러] 공공데이터포털 지난 날씨 조회: {str(e)}')
                        print()
                        continue
                elif weather_menu_number == 2:
                    print('서비스 준비중입니다\n')

                else:
                    info_message = '[알림] 메뉴 목록을 선택해 주세요.\n'
                    print(info_message)
                    continue

        elif main_menu_number == 4:
            """ 코로나19 크롤링 """
            covid19_crawler = Covid19Crawler(data_gov_key=property_reader.get('DATA_GOV_KEY').data)

            while True:
                try:
                    covid19_menu_number = int(input('[알림] 원하는 메뉴를 입력해 주세요.\n0:메인메뉴 | 1:전국예방접종센터 조회 | 2:국가별 이슈\n'))
                except Exception as e:
                    info_message = '[경고] 숫자만 입력해 주세요.\n'
                    print(info_message)
                    continue

                try:
                    if covid19_menu_number == 0:
                        """ 메인 메뉴로 이동 """
                        break

                    elif covid19_menu_number == 1:
                        """ 공공데이터포털 코로나19 예방접종센터 조회 """
                        covid19_search_address = input('[알림] 검색할 지역을 입력해 주세요. 미입력 시 전체 센터 조회\n')
                        covid19_crawler.get_vaccine_center_info_by_address(covid19_search_address=covid19_search_address)

                    elif covid19_menu_number == 2:
                        """ 공공데이터포털 코로나19 예방접종센터 조회 """
                        covid19_nation_name = input('[알림] 검색할 국가를 입력해 주세요: ')
                        covid19_crawler.search_national_issue_by_nation_name(nation_name=covid19_nation_name)

                    else:
                        info_message = '[알림] 메뉴 목록을 선택해 주세요.\n'
                        print(info_message)
                        continue
                except Exception as e:
                    sentry.capture_exception(e)
                    logger.exception(f'[에러] 공공데이터포털 코로나19 예방접종센터 조회: {str(e)}')
                    print()

        elif main_menu_number == 5:
            """ 게임 크롤링 """
            game_crawler = GameCrawler(steam_key=property_reader.get('STEAM_KEY').data,
                                       blizzard_client_name=property_reader.get('BLIZZARD_CLIENT_NAME').data,
                                       blizzard_client_id=property_reader.get('BLIZZARD_CLIENT_ID').data,
                                       blizzard_client_secret=property_reader.get('BLIZZARD_CLIENT_SECRET').data,
                                       blizzard_redirect_url=property_reader.get('BLIZZARD_REDIRECT_URL').data,
                                       blizzard_region=property_reader.get('BLIZZARD_REGION').data,
                                       blizzard_locale=property_reader.get('BLIZZARD_LOCALE').data)
            while True:
                try:
                    game_menu_number = int(input('[알림] 원하는 메뉴를 입력해 주세요.\n0:메인메뉴 | 1:Steam | 2:Blizzard\n'))
                except Exception as e:
                    info_message = '[경고] 숫자만 입력해 주세요.\n'
                    print(info_message)
                    continue

                if game_menu_number == 0:
                    """ 메인 메뉴로 이동 """
                    break

                elif game_menu_number == 1:
                    """ 스팀 메뉴 """
                    while True:
                        try:
                            steam_menu_number = int(input('[알림] 원하는 메뉴를 입력해 주세요.\n0:상위메뉴 | 1:게임조회\n'))
                        except Exception as e:
                            info_message = '[경고] 숫자만 입력해 주세요.\n'
                            print(info_message)
                            continue

                        if steam_menu_number == 0:
                            """ 상위 메뉴로 이동 """
                            break

                        elif steam_menu_number == 1:
                            """ 스팀게임조회 메뉴 """
                            try:
                                game_name = input('[알림] 검색할 게임명(영문 소문자) 입력해 주세요. 미입력 시 전체 게임 조회\n')
                                game_crawler.search_steam_game_name_by_game_name(game_name=game_name)
                            except Exception as e:
                                sentry.capture_exception(e)
                                logger.exception(f'[에러] 스팀게임 조회: {str(e)}')
                                print()

                        else:
                            info_message = '[알림] 메뉴 목록을 선택해 주세요.\n'
                            print(info_message)
                            continue

                elif game_menu_number == 2:
                    """ 블리자드 메뉴 """
                    try:
                        game_crawler.get_new_blizzard_access_token()
                    except Exception as e:
                        sentry.capture_exception(e)
                        logger.exception(f'[에러] 블리자드 토큰 요청: {str(e)}')
                        print()
                        continue

                    while True:
                        try:
                            blizzard_menu_number = int(input('[알림] 원하는 메뉴를 입력해 주세요.\n0:상위메뉴 | 1:디아블로3 | 2:스타크래프트2 | 3:하스스톤 | 4:WOW | 5.WOW Classic\n'))
                        except Exception as e:
                            info_message = '[경고] 숫자만 입력해 주세요.\n'
                            print(info_message)
                            continue

                        if blizzard_menu_number == 0:
                            """ 상위 메뉴로 이동 """
                            break
                        elif blizzard_menu_number == 1:
                            """ 디아블로3 메뉴 """
                            while True:
                                try:
                                    blizzard_diablo_3_menu_number = int(input('[알림] 원하는 메뉴를 입력해 주세요.\n0:상위메뉴 | 1:프로필검색\n'))
                                except Exception as e:
                                    info_message = '[경고] 숫자만 입력해 주세요.\n'
                                    print(info_message)
                                    continue

                                if blizzard_diablo_3_menu_number == 0:
                                    """ 상위 메뉴로 이동 """
                                    break
                                elif blizzard_diablo_3_menu_number == 1:
                                    blizzard_d3_battle_tag = str(input('[알림] 배틀태그를 입력해 프로필 검색: ')).replace('#', '%23')
                                    try:
                                        game_crawler.get_blizzard_diablo_3_profile(d3_battle_tag=blizzard_d3_battle_tag)
                                    except Exception as e:
                                        sentry.capture_exception(e)
                                        logger.exception(f'[에러] 디아블로3 프로필 조회: {str(e)}')
                                        print()
                                else:
                                    info_message = '[알림] 메뉴 목록을 선택해 주세요.\n'
                                    print(info_message)
                                    continue
                        elif blizzard_menu_number == 2:
                            """ 스타크래프트2 메뉴 """
                            print('서비스 준비중입니다\n')
                        elif blizzard_menu_number == 3:
                            """ 하스스톤 메뉴 """
                            print('서비스 준비중입니다\n')
                        elif blizzard_menu_number == 4:
                            """ WOW 메뉴 """
                            print('서비스 준비중입니다\n')
                        elif blizzard_menu_number == 5:
                            """ WOW Classic 메뉴 """
                            print('서비스 준비중입니다\n')
                        else:
                            info_message = '[알림] 메뉴 목록을 선택해 주세요.\n'
                            print(info_message)
                            continue
                else:
                    info_message = '[알림] 메뉴 목록을 선택해 주세요.\n'
                    print(info_message)
                    continue

        elif main_menu_number == 6:
            """ 사건사고 크롤링 """
            accident_crawler = AccidentCrawler(data_gov_key=property_reader.get('DATA_GOV_KEY').data)

            while True:
                try:
                    accident_menu_number = int(input('[알림] 원하는 메뉴를 입력해 주세요.\n0:메인메뉴 | 1:사망교통사고정보\n'))
                except Exception as e:
                    info_message = '[경고] 숫자만 입력해 주세요.\n'
                    print(info_message)
                    continue

                if accident_menu_number == 0:
                    """ 메인 메뉴로 이동 """
                    break

                elif accident_menu_number == 1:
                    """ 사망교통사고정보조회 """
                    try:
                        accident_search_year = int(input('[알림] 조회 년도를 입력하세요: '))
                        accident_search_sido = str(input('[알림] 조회 지역-시/도를 입력하세요: '))
                        accident_search_gugun = str(input('[알림] 조회 지역-시/군/구를 입력하세요: '))
                    except Exception as e:
                        info_message = '[경고] 정확한 값을 입력해 주세요.\n'
                        print(info_message)
                        continue
                    try:
                        accident_search_sido_code = accident_crawler.transfer_search_string_to_code(response_column=1,
                                                                                                    response_value=accident_search_sido)  # 검색에 포함되어 있는 지역을 코드로 변환
                        accident_search_gugun_code = accident_crawler.transfer_search_string_to_code(response_column=2,
                                                                                                     response_value=accident_search_gugun,
                                                                                                     sido_code=accident_search_sido_code)  # 검색에 포함되어 있는 지역을 코드로 변환

                        accident_crawler.get_car_accident_info_by_year_and_location(search_year=accident_search_year, search_sido=accident_search_sido_code, search_gugun=accident_search_gugun_code)
                    except Exception as e:
                        sentry.capture_exception(e)
                        logger.exception(f'[에러] 공공데이터포털 교통사고정보 조회: {str(e)}')
                        print()
                        continue

                else:
                    info_message = '[알림] 메뉴 목록을 선택해 주세요.\n'
                    print(info_message)
                    continue

        elif main_menu_number == 7:
            """ 카카오 크롤링 """
            kakao_crawler = KakaoCrawler(kakao_app_id=property_reader.get('KAKAO_APP_INWOO_ID').data,
                                         kakao_app_name=property_reader.get('KAKAO_APP_INWOO_NAME').data,
                                         kakao_app_native_key=property_reader.get('KAKAO_APP_INWOO_NATIVE_KEY').data,
                                         kakao_app_rest_key=property_reader.get('KAKAO_APP_INWOO_REST_KEY').data,
                                         kakao_app_js_key=property_reader.get('KAKAO_APP_INWOO_JS_KEY').data,
                                         kakao_app_admin_key=property_reader.get('KAKAO_APP_INWOO_ADMIN_KEY').data,
                                         kakao_app_domian=property_reader.get('KAKAO_APP_INWOO_DOMAIN').data,
                                         kakao_app_redirect_uri=property_reader.get('KAKAO_APP_INWOO_REDIRECT_URI').data
                                         )

            try:
                kakao_crawler.get_new_kakao_access_code()
                kakao_app_inwoo_access_code = str(input('[알림] 위 링크에서 카카오 로그인 후 URL에 나타난 code값을 입력해 주세요: '))
            except Exception as e:
                sentry.capture_exception(e)
                logger.exception(f'[에러] 카카오 인가코드 요청: {str(e)}')
                print()
                continue

            try:
                kakao_crawler.get_new_kakao_access_token(kakao_access_code=kakao_app_inwoo_access_code)
            except Exception as e:
                sentry.capture_exception(e)
                logger.exception(f'[에러] 카카오 토큰 요청: {str(e)}')
                print()
                continue

            while True:
                try:
                    kakao_menu_number = int(input('[알림] 원하는 메뉴를 입력해 주세요.\n0:메인메뉴 | 1:토큰정보 | 2:토큰갱신 | 3:사용자목록 | 4:나에게문자보내기 | 5.언어번역\n'))
                except Exception as e:
                    info_message = '[경고] 숫자만 입력해 주세요.\n'
                    print(info_message)
                    continue

                if kakao_menu_number == 0:
                    """ 메인 메뉴로 이동 """
                    break

                elif kakao_menu_number == 1:
                    """ 토큰 정보 조회 """
                    try:
                        kakao_crawler.get_kakao_token_info()
                    except Exception as e:
                        sentry.capture_exception(e)
                        logger.exception(f'[에러] 카카오 사용자 토큰 정보 조회: {str(e)}')
                        print()
                        continue

                elif kakao_menu_number == 2:
                    """ 토큰 갱신 """
                    try:
                        kakao_crawler.refresh_kakao_access_token()
                    except Exception as e:
                        sentry.capture_exception(e)
                        logger.exception(f'[에러] 카카오 사용자 토큰 갱신: {str(e)}')
                        print()
                        continue

                elif kakao_menu_number == 3:
                    """ 앱 사용자 리스트 조회 """
                    try:
                        kakao_crawler.get_kakao_user_list()
                    except Exception as e:
                        sentry.capture_exception(e)
                        logger.exception(f'[에러] 카카오 사용자 목록 조회: {str(e)}')
                        print()
                        continue

                elif kakao_menu_number == 4:
                    """ 나에게 문자보내기 """
                    kakao_text_message = str(input('[알림] 전송할 문자를 입력하세요: '))
                    try:
                        kakao_crawler.kakao_send_message_myself(text_message=kakao_text_message)
                    except Exception as e:
                        sentry.capture_exception(e)
                        logger.exception(f'[에러] 카카오 나에게 문자보내기: {str(e)}')
                        print()
                        continue

                elif kakao_menu_number == 5:
                    """ 카카오 번역 """
                    try:
                        kakao_selected_language_to_translate_num = int(input('[알림] 입력할 언어의 번호를 선택해 주세요:\n1.한국어 2.영어 3.일본어 4.중국어 5.베트남어 6.인도네시아어 7.아랍어 8.뱅갈어 9.독일어 10.스페인어 11.프랑스어 12.힌디어 13.이탈리아어 14.말레이시아어 15.네덜란드어 16.포르투갈어 17.러시아어 18.태국어 19.터키어\n'))
                        kakao_selected_language_to_translated_num = int(input('[알림] 출력할 언어의 번호를 선택해 주세요:\n1.한국어 2.영어 3.일본어 4.중국어 5.베트남어 6.인도네시아어 7.아랍어 8.뱅갈어 9.독일어 10.스페인어 11.프랑스어 12.힌디어 13.이탈리아어 14.말레이시아어 15.네덜란드어 16.포르투갈어 17.러시아어 18.태국어 19.터키어\n'))

                        if kakao_selected_language_to_translate_num < 1 or kakao_selected_language_to_translate_num > 19 or kakao_selected_language_to_translated_num < 1 or kakao_selected_language_to_translated_num > 19:
                            info_message = '[알림] 목록에 존재하는 번호를 선택해 주세요.\n'
                            print(info_message)
                            continue
                    except Exception as e:
                        info_message = '[경고] 숫자만 입력해 주세요.\n'
                        print(info_message)
                        continue

                    kakao_text_to_translate = str(input('[알림] 번역할 내용을 입력해 주세요: '))

                    try:
                        kakao_crawler.kakao_translate(language_num_to_translate=kakao_selected_language_to_translate_num, language_num_to_translated=kakao_selected_language_to_translated_num, text_to_translate=kakao_text_to_translate)
                    except Exception as e:
                        sentry.capture_exception(e)
                        logger.exception(f'[에러] 카카오 나에게 문자보내기: {str(e)}')
                        print()
                        continue

                else:
                    info_message = '[알림] 메뉴 목록을 선택해 주세요.\n'
                    print(info_message)
                    continue

        elif main_menu_number == 8:
            """ 챗봇 크롤링 """
            chat_bot_crawler = ChatBotCrawler(simsimi_api_key=property_reader.get('SIMSIMI_DEMO_APP_KEY').data, simsimi_version=property_reader.get('SIMSIMI_VERSION').data)

            while True:
                try:
                    chat_bot_menu_number = int(input('[알림] 원하는 메뉴를 입력해 주세요.\n0:메인메뉴 | 1:심심이와 대화\n'))
                except Exception as e:
                    info_message = '[경고] 숫자만 입력해 주세요.\n'
                    print(info_message)
                    continue

                if chat_bot_menu_number == 0:
                    """ 메인 메뉴로 이동 """
                    break

                elif chat_bot_menu_number == 1:
                    try:
                        simsimi_selected_language_code = int(input('[알림] 심심이와 대화을 시작합니다. 언어를 선택해 주세요. 1:Korean 2:English\n'))
                    except Exception as e:
                        info_message = '[경고] 숫자만 입력해 주세요.\n'
                        print(info_message)
                        continue

                    if simsimi_selected_language_code == 1:
                        print('"종료" 입력 시 대화 종료')
                        while True:
                            now_time = time.strftime('%Y-%m-%d %H:%M:%S')
                            chat_message = str(input('보낼 메시지: '))
                            if chat_message == '종료':
                                print()
                                break
                            print('[{0}] 나: {1}'.format(now_time.split()[1], chat_message))
                            chat_bot_crawler.chat_with_simsimi(chat_message=chat_message, language_type='ko')
                    elif simsimi_selected_language_code == 2:
                        print('Write "exit" to end chatting')
                        while True:
                            now_time = time.strftime('%Y-%m-%d %H:%M:%S')
                            chat_message = str(input('Message to send: '))
                            if chat_message == 'exit':
                                print()
                                break
                            print('[{0}] me: {1}'.format(now_time.split()[1], chat_message))
                            chat_bot_crawler.chat_with_simsimi(chat_message=chat_message, language_type='en')
                    else:
                        info_message = '[알림] 메뉴 목록을 선택해 주세요.\n'
                        print(info_message)
                        continue

                else:
                    info_message = '[알림] 메뉴 목록을 선택해 주세요.\n'
                    print(info_message)
                    continue
        elif main_menu_number == 9:
            """ 경기도 정보 크롤링 """
            gyeonggi_info_crawler = GyeonggiInfoCrawler(data_gg_gov_key=property_reader.get('DATA_GG_GOV_KEY').data)
            # 경기도 주소 정보 딕셔너리
            gyeonggi_address_dict = {
                'sigun': ['가평군', '고양시', '과천시', '광명시', '광주시', '구리시', '군포시', '김포시', '남양주시', '동두천시', '부천시', '성남시', '수원시',
                          '시흥시', '안산시', '안성시', '안양시', '양주시', '양평군', '여주시', '연천군', '오산시', '용인시', '의왕시', '의정부시', '이천시',
                          '파주시', '평택시', '포천시', '하남시', '화성시']}

            while True:
                try:
                    gyeonggi_info_menu_number = int(input('[알림] 원하는 메뉴를 입력해 주세요.\n0:메인메뉴 | 1:CCTV 현황 | 2:지역화폐 정보 | 3:무료와이파이 정보 | 4:공중화장실 현황 | 5:전기차충전소 현황 |\n'))
                except Exception as e:
                    info_message = '[경고] 숫자만 입력해 주세요.\n'
                    print(info_message)
                    continue

                if gyeonggi_info_menu_number == 0:
                    """ 메인 메뉴로 이동 """
                    break

                elif gyeonggi_info_menu_number == 1:
                    """ CCTV 현황 조회 """
                    try:
                        gyeonggi_search_sigun_name = str(input('[알림] 시군명을 입력해주세요 ex)성남시: '))
                        if gyeonggi_search_sigun_name not in gyeonggi_address_dict['sigun']:
                            info_message = '[알림] 정확한 시군명을 입력해 주세요.\n'
                            print(info_message)
                            continue
                        gyeonggi_info_crawler.get_cctv_installation_info(gyeonggi_search_sigun_name=gyeonggi_search_sigun_name)
                    except Exception as e:
                        sentry.capture_exception(e)
                        logger.exception(f'[에러] 경기데이터드림 CCTV 설치 현황 조회: {str(e)}')
                        print()
                        continue

                elif gyeonggi_info_menu_number == 2:
                    """ 지역화폐 가맹점 조회 """
                    try:
                        gyeonggi_search_sigun_name = str(input('[알림] 시군명을 입력해주세요 ex)성남시: '))
                        if gyeonggi_search_sigun_name not in gyeonggi_address_dict['sigun']:
                            info_message = '[알림] 정확한 시군명을 입력해 주세요.\n'
                            print(info_message)
                            continue
                        gyeonggi_info_crawler.get_local_store_info(gyeonggi_search_sigun_name=gyeonggi_search_sigun_name)
                    except Exception as e:
                        sentry.capture_exception(e)
                        logger.exception(f'[에러] 경기데이터드림 지역화폐 가맹점 현황 조회: {str(e)}')
                        print()
                        continue

                elif gyeonggi_info_menu_number == 3:
                    """ 무료 와이파이 사용가능 장소 조회 """
                    try:
                        gyeonggi_search_sigun_name = str(input('[알림] 시군명을 입력해주세요 ex)성남시: '))
                        if gyeonggi_search_sigun_name not in gyeonggi_address_dict['sigun']:
                            info_message = '[알림] 정확한 시군명을 입력해 주세요.\n'
                            print(info_message)
                            continue
                        gyeonggi_info_crawler.get_free_wifi_info(gyeonggi_search_sigun_name=gyeonggi_search_sigun_name)
                    except Exception as e:
                        sentry.capture_exception(e)
                        logger.exception(f'[에러] 경기데이터드림 무료 와이파이 사용가능 장소 조회: {str(e)}')
                        print()
                        continue

                elif gyeonggi_info_menu_number == 4:
                    """ 공중화장실 현황 조회 """
                    try:
                        gyeonggi_search_sigun_name = str(input('[알림] 시군명을 입력해주세요 ex)성남시: '))
                        if gyeonggi_search_sigun_name not in gyeonggi_address_dict['sigun']:
                            info_message = '[알림] 정확한 시군명을 입력해 주세요.\n'
                            print(info_message)
                            continue
                        gyeonggi_info_crawler.get_public_toilet_info(gyeonggi_search_sigun_name=gyeonggi_search_sigun_name)
                    except Exception as e:
                        sentry.capture_exception(e)
                        logger.exception(f'[에러] 경기데이터드림 공중화장실 현황 조회: {str(e)}')
                        print()
                        continue

                elif gyeonggi_info_menu_number == 5:
                    """ 전기차 충전소 현황 조회 """
                    try:
                        gyeonggi_search_sigun_name = str(input('[알림] 시군명을 입력해주세요 ex)성남시: '))
                        if gyeonggi_search_sigun_name not in gyeonggi_address_dict['sigun']:
                            info_message = '[알림] 정확한 시군명을 입력해 주세요.\n'
                            print(info_message)
                            continue
                        gyeonggi_info_crawler.get_electric_gas_station_info(gyeonggi_search_sigun_name=gyeonggi_search_sigun_name)
                    except Exception as e:
                        sentry.capture_exception(e)
                        logger.exception(f'[에러] 경기데이터드림 전기차 충전소 현황 조회: {str(e)}')
                        print()
                        continue
        else:
            info_message = '[알림] 메뉴 목록을 선택해 주세요.\n'
            print(info_message)
            continue

    print('[출처] 영화진흥위원회, FLO, 공공데이터포털, SteamWorks, Kakao developers')
