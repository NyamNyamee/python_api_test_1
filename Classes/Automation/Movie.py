import time
import requests
import json

from Classes.Util.UnicodeUtil import *


class MovieCrawler:
    """ 영화정보 크롤러 """

    def __init__(self, kofic_key):
        self.kofic_key = kofic_key

    def get_box_office_list_by_date(self, target_date=str(int(time.strftime('%Y%m%d')) - 1)):
        """ 날짜로 박스오피스 검색 """
        # url생성
        url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={0}&targetDt={1}'.format(
            self.kofic_key, target_date)

        try:
            # 요청보내고 응답 저장
            res = requests.get(url)
            # 응답의 텍스트
            res_text = res.text
            # 응답의 텍스트를 json형태로 파싱
            parsed_object = json.loads(res_text)
            # 위 두줄을 아래와 같이 사용해도 됨
            # parsed_object = res.json()
        except Exception as e:
            raise RuntimeError('영화진흥위원회로부터 정보를 가져오는 데에 실패했습니다.')

        # 박스오피스 리스트만 가져옴
        list_box_office = parsed_object['boxOfficeResult']['dailyBoxOfficeList']

        # 결과출력
        print('순위   |    개봉일    |    누적매출액    |    누적관객수    |    해당일자 상영횟수    |    제목')
        for index, component in enumerate(list_box_office):
            movie_rank = component['rank']
            movie_name = component['movieNm']
            movie_open_date = component['openDt']
            movie_sales_account = component['salesAcc']
            movie_audience_account = component['audiAcc']
            movie_show_count = component['showCnt']
            print('{0:8}{1:12}{2:18}{3:17}{4:23}{5}'.format(movie_rank,
                                                            movie_open_date,
                                                            format(int(movie_sales_account), ','),
                                                            format(int(movie_audience_account), ','),
                                                            format(int(movie_show_count), ','),
                                                            movie_name))
        print()

    def get_movie_list_by_movie_name(self, movie_name):
        """ 영화 제목으로 영화 목록 검색 """
        # url생성
        url = 'http://kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key={0}&movieNm={1}'.format(
            self.kofic_key, movie_name)

        try:
            # 요청보내고 응답 저장
            res = requests.get(url)
            # 응답의 텍스트
            res_text = res.text
            # 응답의 텍스트를 json형태로 파싱
            parsed_object = json.loads(res_text)
            # 위 두줄을 아래와 같이 사용해도 됨
            # parsed_object = res.json()
        except Exception as e:
            raise RuntimeError('영화진흥위원회로부터 정보를 가져오는 데에 실패했습니다.')

        # 조회 결과
        dict_movie_result = parsed_object['movieListResult']

        # 검색영화 리스트만 가져옴
        list_movie_search = dict_movie_result['movieList']

        # 검색 개수가 0개라면
        if not list_movie_search:
            print('검색 결과가 없습니다.\n')
            return

        # 영화상세정보를 검색하기 위해 영화코드를 저장할 리스트
        list_movie_code = []

        # 결과출력
        print('번호    |    제작연도    |    개봉일    |        장르        |    제작국가    |        감독        |    제목(국문)')
        for index, component in enumerate(list_movie_search):
            movie_code = component['movieCd']
            list_movie_code.append(movie_code)

            movie_name_kor = component['movieNm']
            movie_prod_year = component['prdtYear']
            movie_open_date = component['openDt']
            movie_genre = component['genreAlt']
            movie_prod_nation = component['repNationNm']
            list_movie_director = component['directors']
            movie_director = 'unknown' if not list_movie_director else list_movie_director[0]['peopleNm']

            print('{0:8}{1:15}{2:14}{3}{4}{5}{6}'.format(str(index + 1),
                                                         movie_prod_year,
                                                         movie_open_date,
                                                         UnicodeUtil.fill_str_with_space(string=movie_genre,
                                                                                         max_size=24),
                                                         UnicodeUtil.fill_str_with_space(string=movie_prod_nation,
                                                                                         max_size=16),
                                                         UnicodeUtil.fill_str_with_space(string=movie_director,
                                                                                         max_size=22),
                                                         movie_name_kor
                                                         ))

        # 영화목록에서 빼낸 영화코드 리스트를 담아 영화상세정보검색 함수 호출
        self.get_detail_movie_info_by_movie_code(list_movie_code)

    def get_detail_movie_info_by_movie_code(self, list_movie_code):
        """ 영화 코드로 영화 상세정보 검색 """
        try:
            # 사용자가 번호 선택
            selected_movie_code = int(input('영화 상세정보를 보시려면 번호를 입력해주세요. (0입력 시 메뉴로 이동)\n'))
            # 0 이하거나, 영화목록 개수보다 큰 수를 입력했을 때 리턴
            if selected_movie_code <= 0 or selected_movie_code > len(list_movie_code):
                print()
                return
        except Exception as e:
            print()
            return

        # url생성
        url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={0}&movieCd={1}'.format(
            self.kofic_key, list_movie_code[selected_movie_code - 1])
        try:
            # 요청보내고 응답 저장
            res = requests.get(url)
            # 응답의 텍스트
            res_text = res.text
            # 응답의 텍스트를 json형태로 파싱
            parsed_object = json.loads(res_text)
            # 위 두줄을 아래와 같이 사용해도 됨
            # parsed_object = res.json()
        except Exception as e:
            raise RuntimeError('영화진흥위원회로부터 정보를 가져오는 데에 실패했습니다.')

        movie_info_dict = parsed_object['movieInfoResult']['movieInfo']

        # 결과출력
        print('러닝타임    |    제작연도    |    개봉일자    |        감독        |        제목(국문)        |        제목(영문)')
        detail_movie_name_kor = movie_info_dict['movieNm']
        detail_movie_movie_name_eng = movie_info_dict['movieNmEn']
        detail_movie_movie_show_time = movie_info_dict['showTm']
        detail_movie_movie_prod_year = movie_info_dict['prdtYear']
        detail_movie_movie_open_date = movie_info_dict['openDt']
        list_detail_movie_movie_directors = movie_info_dict['directors']
        detail_movie_movie_director = 'unknown' if not list_detail_movie_movie_directors else list_detail_movie_movie_directors[0]['peopleNm']

        print('{0:11}{1:16}{2:15}{3}{4}{5}'.format(
            detail_movie_movie_show_time,
            detail_movie_movie_prod_year,
            detail_movie_movie_open_date,
            UnicodeUtil.fill_str_with_space(string=detail_movie_movie_director, max_size=22),
            UnicodeUtil.fill_str_with_space(string=detail_movie_name_kor, max_size=40),
            UnicodeUtil.fill_str_with_space(string=detail_movie_movie_name_eng, max_size=40),
        ))
        print()

    def get_movie_person_by_person_name(self, person_name):
        """ 이름으로 영화인 목록 검색 """
        # url생성
        url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key={0}&peopleNm={1}'.format(
            self.kofic_key, person_name)

        try:
            # 요청보내고 응답 저장
            res = requests.get(url)
            # 응답의 텍스트
            res_text = res.text
            # 응답의 텍스트를 json형태로 파싱
            parsed_object = json.loads(res_text)
            # 위 두줄을 아래와 같이 사용해도 됨
            # parsed_object = res.json()
        except Exception as e:
            raise RuntimeError('영화진흥위원회로부터 정보를 가져오는 데에 실패했습니다.')

        # 검색 결과
        dict_people_result = parsed_object['peopleListResult']

        # 영화인 리스트만 가져옴
        list_people_search = dict_people_result['peopleList']

        # 검색 개수가 0개라면
        if not list_people_search:
            print('검색 결과가 없습니다.\n')
            return

        # 결과출력
        print('번호    |    이름    |        이름(영문)        |        역할        |    필모그래피')
        for index, component in enumerate(list_people_search):
            people_name_kor = component['peopleNm']
            people_name_eng = component['peopleNmEn']
            people_role_name = component['repRoleNm']
            people_filmography_names = component['filmoNames']

            print('{0:8}{1}{2}{3}{4}'.format(str(index + 1),
                                             UnicodeUtil.fill_str_with_space(string=people_name_kor, max_size=13),
                                             UnicodeUtil.fill_str_with_space(string=people_name_eng, max_size=26),
                                             UnicodeUtil.fill_str_with_space(string=people_role_name, max_size=22),
                                             people_filmography_names
                                             ))
        print()



