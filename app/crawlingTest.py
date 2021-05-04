import sys
import time

import jproperties

from Classes.Automation.Movie import MovieCrawler
from Classes.Automation.Music import MusicCrawler
from Classes.Automation.Weather import WeatherCrawler
from Classes.Automation.Covid19 import Covid19Crawler
from Classes.Automation.Game import GameCrawler
from Classes.Automation.Accident import AccidentCrawler
from Classes.Automation.Kakao import KakaoCrawler

if __name__ == '__main__':
    property_reader = jproperties.Properties()

    try:
        with open('../resources/auth.properties', 'rb') as auth_properties:
            property_reader.load(auth_properties)
    except Exception as e:
        print('[에러] cannot open .properties file')

    while True:
        try:
            main_menu_number = int(input('[알림] 원하는 메뉴를 입력해 주세요.\n0:프로그램종료 | 1:영화검색 | 2:음악검색 | 3:날씨검색 | 4:코로나19정보 | 5:게임정보 | 6:사건사고정보 | 7:카카오\n'))
        except Exception as e:
            print('[경고] 숫자만 입력해 주세요.\n')
            continue

        if main_menu_number == 0:
            """ 프로그램 종료 """
            break

        elif main_menu_number == 1:
            """ 영화정보 크롤링 """
            movie_crawler = MovieCrawler(kofic_key=property_reader.get('KOFIC_KEY').data)

            try:
                movie_menu_number = int(input('[알림] 원하는 메뉴를 입력해 주세요.\n0:메인메뉴 | 1:박스오피스검색 | 2:영화검색 | 3:영화인검색\n'))
            except Exception as e:
                print('[경고] 숫자만 입력해 주세요.\n')
                continue

            if movie_menu_number == 0:
                """ 메인 메뉴로 이동 """
                continue

            elif movie_menu_number == 1:
                """ 영화진흥위원회 박스오피스 조회 """
                target_date = input('[알림] 조회할 날짜를 입력하세요. ex)2021-04-20\n').replace('-', '').strip()

                try:
                    if len(target_date) != 8:
                        print('[알림] 연월일을 yyyy-MM-dd 형태로 입력해 주세요.\n')
                        continue
                    if int(target_date) > int(time.strftime('%Y%m%d')) - 1:
                        print('[알림] 오늘 날짜 이상은 입력하실 수 없습니다.\n')
                        continue

                    movie_crawler.get_box_office_list_by_date(target_date=target_date)
                except Exception as e:
                    print()
                    continue

            elif movie_menu_number == 2:
                """ 영화진흥위원회 영화 목록, 상세정보 검색 """
                movie_name = input('[알림] 검색할 영화제목을 입력하세요: ').strip()
                try:
                    movie_crawler.get_movie_list_by_movie_name(movie_name=movie_name)
                except Exception as e:
                    print()
                    continue

            elif movie_menu_number == 3:
                """ 영화진흥위원회 영화인 목록 검색 """
                person_name = input('[알림] 검색할 영화인 이름을 입력하세요: ').strip()
                try:
                    movie_crawler.get_movie_person_by_person_name(person_name=person_name)
                except Exception as e:
                    print()
                    continue

            else:
                print('[알림] 메뉴 목록을 선택해 주세요.\n')
                continue

        elif main_menu_number == 2:
            """ 음악정보 크롤링 """
            music_crawler = MusicCrawler()

            try:
                music_menu_number = int(input('[알림] 원하는 메뉴를 입력해 주세요.\n0:메인메뉴 | 1:최신100곡(국내) | 2:최신100곡(해외)\n'))
            except Exception as e:
                print('[경고] 숫자만 입력해 주세요.\n')
                continue

            if music_menu_number == 0:
                """ 메인 메뉴로 이동 """
                continue

            elif music_menu_number == 1:
                """ FLO 최신곡(국내) 조회 """
                location = 'KPOP'
                music_crawler.get_latest_song(location=location)

            elif music_menu_number == 2:
                """ FLO 최신곡(해외) 조회 """
                location = 'POP'
                music_crawler.get_latest_song(location=location)

        elif main_menu_number == 3:
            """ 날씨정보 크롤링 """
            weather_crawler = WeatherCrawler(data_gov_key=property_reader.get('DATA_GOV_KEY').data)

            try:
                weather_menu_number = int(input('[알림] 원하는 메뉴를 입력해 주세요.\n0:메인메뉴 | 1:지난 날씨정보 | 2:오늘 날씨정보\n'))
            except Exception as e:
                print('[경고] 숫자만 입력해 주세요.\n')
                continue

            if weather_menu_number == 0:
                """ 메인 메뉴로 이동 """
                continue

            elif weather_menu_number == 1:
                """ 공공데이터포털 지난 날씨정보 검색 """
                start_date = input('[알림] 조회할 날짜를 입력하세요. ex)2021-04-20\n').replace('-', '').strip()

                try:
                    end_date = int(start_date) + 1  # 조회 시작날짜 + 1
                except Exception as e:
                    print('[경고] 숫자만 입력해 주세요.\n')
                    continue

                if len(start_date) != 8:
                    print('[알림] 연월일을 yyyy-MM-dd 형태로 입력해 주세요.\n')
                    continue
                if int(start_date) > int(time.strftime('%Y%m%d')) - 2:
                    print('[알림] 어제 날씨 정보 조회 시, 그저께 날짜를 입력해 주세요.\n')
                    continue
                if int(start_date) < 19071001:
                    print('[알림] 1907-10-01 이전 날짜는 조회할 수 없습니다.\n')
                    continue

                weather_location = 108  # 지점코드(서울 임시 고정)

                try:
                    weather_crawler.get_ex_weather_info(start_date=start_date, end_date=end_date,
                                                        weather_location=weather_location)
                except Exception as e:
                    print()
                    continue
            elif weather_menu_number == 2:
                print('오늘날씨 검색 시작해야함')

            else:
                print('[알림] 메뉴 목록을 선택해 주세요.\n')
                continue

        elif main_menu_number == 4:
            """ 코로나19 크롤링 """
            covid19_crawler = Covid19Crawler(data_gov_key=property_reader.get('DATA_GOV_KEY').data)

            try:
                covid19_menu_number = int(input('[알림] 원하는 메뉴를 입력해 주세요.\n0:메인메뉴 | 1:전국예방접종센터 조회 | 2:국가별 이슈\n'))
            except Exception as e:
                print('[경고] 숫자만 입력해 주세요.\n')
                continue

            if covid19_menu_number == 0:
                """ 메인 메뉴로 이동 """
                continue

            elif covid19_menu_number == 1:
                """ 공공데이터포털 코로나19 예방접종센터 조회 """
                covid19_search_address = input('[알림] 검색할 지역을 입력해 주세요. 미입력 시 전체 센터 조회\n')
                covid19_crawler.get_vaccine_center_info_by_address(covid19_search_address=covid19_search_address)

            elif covid19_menu_number == 2:
                """ 공공데이터포털 코로나19 예방접종센터 조회 """
                covid19_nation_name = input('[알림] 검색할 국가를 입력해 주세요: ')
                covid19_crawler.search_national_issue_by_nation_name(nation_name=covid19_nation_name)

            else:
                print('[알림] 메뉴 목록을 선택해 주세요.\n')
                continue

        elif main_menu_number == 5:
            """ 게임 크롤링 """
            game_crawler = GameCrawler(steam_key=property_reader.get('STEAM_KEY').data)

            try:
                game_menu_number = int(input('[알림] 원하는 메뉴를 입력해 주세요.\n0:메인메뉴 | 1:스팀게임조회\n'))
            except Exception as e:
                print('[경고] 숫자만 입력해 주세요.\n')
                continue

            if game_menu_number == 0:
                """ 메인 메뉴로 이동 """
                continue

            elif game_menu_number == 1:
                """ 스팀게임조회 """
                game_name = input('[알림] 검색할 게임명(영문 소문자) 입력해 주세요. 미입력 시 전체 게임 조회\n')
                game_crawler.search_steam_game_name_by_game_name(game_name=game_name)

            else:
                print('[알림] 메뉴 목록을 선택해 주세요.\n')
                continue

        elif main_menu_number == 6:
            """ 사건사고 크롤링 """
            accident_crawler = AccidentCrawler(data_gov_key=property_reader.get('DATA_GOV_KEY').data)

            try:
                accident_menu_number = int(input('[알림] 원하는 메뉴를 입력해 주세요.\n0:메인메뉴 | 1:사망교통사고정보\n'))
            except Exception as e:
                print('[경고] 숫자만 입력해 주세요.\n')
                continue

            if accident_menu_number == 0:
                """ 메인 메뉴로 이동 """
                continue

            elif accident_menu_number == 1:
                """ 사망교통사고정보조회 """
                try:
                    accident_search_year = int(input('[알림] 조회 년도를 입력하세요: '))
                    accident_search_sido = str(input('[알림] 조회 지역-시/도를 입력하세요: '))
                    accident_search_gugun = str(input('[알림] 조회 지역-시/군/구를 입력하세요: '))
                except Exception as e:
                    print('[경고] 정확한 값을 입력해 주세요.\n')
                    continue
                try:
                    accident_search_sido_code = accident_crawler.transfer_search_string_to_code(response_column=1,
                                                                                                response_value=accident_search_sido)  # 검색에 포함되어 있는 지역을 코드로 변환
                    accident_search_gugun_code = accident_crawler.transfer_search_string_to_code(response_column=2,
                                                                                                 response_value=accident_search_gugun,
                                                                                                 sido_code=accident_search_sido_code)  # 검색에 포함되어 있는 지역을 코드로 변환
                except Exception as e:
                    print(str(e))
                    print()
                    continue
                accident_crawler.get_car_accident_info_by_year_and_location(search_year=accident_search_year,
                                                                            search_sido=accident_search_sido_code,
                                                                            search_gugun=accident_search_gugun_code)

            else:
                print('[알림] 메뉴 목록을 선택해 주세요.\n')
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
                print(str(e))
                print()
                continue

            try:
                kakao_access_token = kakao_crawler.get_new_kakao_token(kakao_access_code=kakao_app_inwoo_access_code)

            except Exception as e:
                print(str(e))
                print()
                continue

            while True:
                try:
                    kakao_menu_number = int(input('[알림] 원하는 메뉴를 입력해 주세요.\n0:메인메뉴 | 1:사용자정보 | 2:사용자토큰정보 | 3:나에게문자보내기\n'))
                except Exception as e:
                    print('[경고] 숫자만 입력해 주세요.\n')
                    continue

                if kakao_menu_number == 0:
                    """ 메인 메뉴로 이동 """
                    break

                elif kakao_menu_number == 1:
                    """ 사용자 정보조회 """
                    try:
                        kakao_crawler.get_kakao_user_info(kakao_token=kakao_access_token)
                    except Exception as e:
                        print(str(e))
                        print()
                        continue

                elif kakao_menu_number == 2:
                    """ 사용자 토큰 정보조회 """
                    try:
                        kakao_crawler.get_kakao_token_info(kakao_token=kakao_access_token)
                    except Exception as e:
                        print(str(e))
                        print()
                        continue

                elif kakao_menu_number == 3:
                    """ 나에게 문자보내기 """
                    kakao_text_message = str(input('[알림] 전송할 문자를 입력하세요: '))
                    try:
                        kakao_crawler.kakao_send_message_myself(kakao_token=kakao_access_token, text_message=kakao_text_message)
                    except Exception as e:
                        print(str(e))
                        print()
                        continue

                else:
                    print('[알림] 메뉴 목록을 선택해 주세요.\n')
                    continue
        else:
            print('[알림] 메뉴 목록을 선택해 주세요.\n')
            continue

    print('[출처] 영화진흥위원회, FLO, 공공데이터포털, SteamWorks, Kakao developers')
