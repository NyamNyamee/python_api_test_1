import sys
import time

from Classes.Automation.Movie import MovieCrawler
from Classes.Automation.Music import MusicCrawler
from Classes.Automation.Weather import WeatherCrawler
from Classes.Automation.Covid19 import Covid19Crawler

if __name__ == '__main__':
    while True:
        try:
            main_menu_number = int(input('[알림] 원하는 메뉴를 입력해 주세요.\n0:프로그램종료 | 1:영화검색 | 2:최신곡리스트 | 3:수도권 날씨정보 | 4:코로나19 정보\n'))
        except Exception as e:
            print('[경고] 숫자만 입력해 주세요.\n')
            continue
        
        if main_menu_number == 0:
            """ 프로그램 종료 """
            break

        elif main_menu_number == 1:
            """ 영화정보 크롤링 """
            kofic_key = 'ba4bcd991407f6c2f27ec9244f5f9df7'  # 영화진흥위원회 key

            movie_crawler = MovieCrawler(kofic_key=kofic_key)

            try:
                movie_menu_number = int(input('[알림] 원하는 메뉴를 입력해 주세요.\n0:메인메뉴 | 1:박스오피스검색 | 2:영화검색 | 3:영화인검색\n'))
            except Exception as e:
                print('[경고] 숫자만 입력해 주세요.\n')
                continue

            if movie_menu_number == 0:
                """ 메인 메뉴로 이동 """
                continue

            elif movie_menu_number == 1:
                """ 영화진흥위원회 박스오피스 크롤링 """
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
                """ 영화진흥위원회 영화 목록, 상세정보 크롤링 """
                movie_name = input('[알림] 검색할 영화제목을 입력하세요.\n').strip()
                try:
                    movie_crawler.get_movie_list_by_movie_name(movie_name=movie_name)
                except Exception as e:
                    print()
                    continue

            elif movie_menu_number == 3:
                """ 영화진흥위원회 영화인 목록 크롤링 """
                person_name = input('[알림] 검색할 영화인 이름을 입력하세요.\n').strip()
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
                music_menu_number = int(input('[알림] 원하는 메뉴를 입력해 주세요.\n0:메인메뉴 | 1:국내 | 2:해외\n'))
            except Exception as e:
                print('[경고] 숫자만 입력해 주세요.\n')
                continue

            if music_menu_number == 0:
                """ 메인 메뉴로 이동 """
                continue

            elif music_menu_number == 1:
                """ FLO 최신곡(국내) """
                location = 'KPOP'
                music_crawler.get_latest_song(location=location)

            elif music_menu_number == 2:
                """ FLO 최신곡(해외) """
                location = 'POP'
                music_crawler.get_latest_song(location=location)

        elif main_menu_number == 3:
            """ 날씨정보 크롤링 """
            data_gov_key = 'c%2F4Fz%2BWXkuRo%2F%2BhAuE8b3Bp6iMGrThZOhKKG4DCUNYizAbD8d6xb0VxxQi1HjV1RdQbVFIu8Kb%2BdJ%2FG3jLAY8A%3D%3D'  # 공공데이터포털  key

            weather_crawler = WeatherCrawler(data_gov_key=data_gov_key)

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
                    weather_crawler.get_ex_weather_info(start_date=start_date, end_date=end_date, weather_location=weather_location)
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
            data_gov_key = 'c%2F4Fz%2BWXkuRo%2F%2BhAuE8b3Bp6iMGrThZOhKKG4DCUNYizAbD8d6xb0VxxQi1HjV1RdQbVFIu8Kb%2BdJ%2FG3jLAY8A%3D%3D'  # 공공데이터포털  key

            covid19_crawler = Covid19Crawler(data_gov_key=data_gov_key)

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
                covid19_nation_name = input('[알림] 검색할 국가를 입력해 주세요\n')
                covid19_crawler.search_national_issue_by_nation_name(nation_name=covid19_nation_name)

            else:
                print('[알림] 메뉴 목록을 선택해 주세요.\n')
                continue

        else:
            print('[알림] 메뉴 목록을 선택해 주세요.\n')
            continue
            
    print('[출처] 영화진흥위원회, FLO, 공공데이터포털')
