import sys
import json
import time
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import IEDriverManager

import psutil


def kill_chrome_driver_process():
    """ 크롬드라이버 종료 """
    for process in psutil.process_iter():
        try:
            process_name = process.name()
            process_id = process.pid

            if process_name == 'chromedriver.exe':
                parent_pid = process_id
                parent = psutil.Process(parent_pid)
                # for child in parent.children(recursive=True):  # 자식-부모 종료
                #     child.kill()
                parent.kill()

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def kill_ie_driver_process():
    """ IE드라이버 종료 """
    for process in psutil.process_iter():
        try:
            process_name = process.name()
            process_id = process.pid

            if process_name == 'IEDriverServer.exe':
                parent_pid = process_id
                parent = psutil.Process(parent_pid)
                # for child in parent.children(recursive=True):  # 자식-부모 종료
                #     child.kill()
                parent.kill()

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


# ◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ 20210330 한울 일산말소 등기필 유효성검증 매크로 테스트 시작 ◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆
# """ 전산에서 파라미터 받아오기 """
# original_parameter_string = sys.argv[1].replace('hbcncverifypasswordpy://', '').replace('/', '')
# arg1 = original_parameter_string.split(',')[0]
# arg2 = original_parameter_string.split(',')[1]
# print('고유번호 = ' + arg1)
# print('일련번호 = ' + arg2)
#
# """ 변수 """
# # 인터넷등기소 - 등기필정보관리
# URL = 'http://www.iros.go.kr/b112/rcm/selectERCMGetRgsCodePotalJ.do'
# # 대기시간
# SLEEP_SEC = 5
# # 부동산고유번호 ex)1761-1996-614495
# real_estate_number = arg1
# # 일련번호 ex)2CKG-RAZY-ZZGK
# serial_number = arg2
#
# """ 웹 엘리먼트 """
# REAL_ESTATE_NUMBER = (By.ID, 'id_txt_pin')
# SERIAL_NUMBER = (By.ID, 'id_txt_regi_cert')
# SEARCH_BTN = (By.ID, 'btn_pw_cfrm')
#
# """ 크롬 세팅 """
# # driver = webdriver.Chrome(ChromeDriverManager().install())
#
# """ IE 세팅 """
# driver = webdriver.Ie(IEDriverManager().install())
#
# """ 브라우저 오픈 """
# driver.get(URL)
#
# """ 페이지 로딩 대기 """
# driver.execute_script('return document.readyState == "complete";')
#
# """ 부동산고유번호 입력 """
# input_real_estate_number = driver.find_element(*REAL_ESTATE_NUMBER)
# driver.execute_script("arguments[0].value = '" + real_estate_number + "';", input_real_estate_number)
#
# """ 일련번호 입력 """
# input_serial_number = driver.find_element(*SERIAL_NUMBER)
# driver.execute_script("arguments[0].value = '" + serial_number + "';", input_serial_number)
#
# """ 검색버튼 클릭 """
# button_search = driver.find_element(*SEARCH_BTN)
# driver.execute_script("arguments[0].click();", button_search)
#
# """ 대기(초) """
# # time.sleep(SLEEP_SEC)
#
# """ 브라우저, 드라이버 종료 """
# # driver.quit()
# kill_ie_driver_process()
# ◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ 20210330 한울 일산말소 등기필 유효성검증 매크로 테스트 종료 ◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆


# ◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ 20210331 셀레니움 미세먼지 테스트 시작 ◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆
# """ 변수 """
# # 오픈할 URL
# URL = 'https://www.naver.com'
# # 대기시간
# SLEEP_SEC = 5
# # 검색 키워드
# search_keyword = '미세먼지'
# # 오늘 미세먼지 정보 딕셔너리
# fine_dust_info_dict_today = {}
# # 오늘 미세먼지 정보 리스트
# fine_dust_info_list_today = []
# # 오늘 초미세먼지 정보 딕셔너리
# micro_fine_dust_info_dict_today = {}
# # 오늘 초미세먼지 정보 리스트
# micro_fine_dust_info_list_today = []
#
# # 내일 미세먼지 정보 딕셔너리
# fine_dust_info_dict_tomorrow = {}
# # 내일 미세먼지 정보 리스트
# fine_dust_info_list_tomorrow = []
# # 내일 초미세먼지 정보 딕셔너리
# micro_fine_dust_info_dict_tomorrow = {}
# # 내일 초미세먼지 정보 리스트
# micro_fine_dust_info_list_tomorrow = []
#
# """ 웹 엘리먼트 """
# INPUT_SEARCH = (By.ID, 'query')  # 네이버 검색창
# BUTTON_SEARCH = (By.ID, 'search_btn')  # 검색버튼
# TRS_FINE_DUST_TODAY = (By.CSS_SELECTOR,
#                        '#main_pack > section.sc_new._atmospheric_environment > div > div.api_cs_wrap > div > div:nth-child(3) > div.main_box > div.detail_box > div.tb_scroll > table > tbody > tr')  # 현재 미세먼지 rows
# LI_TOMORROW = (By.CSS_SELECTOR,
#                '#main_pack > section.sc_new._atmospheric_environment > div > div.api_cs_wrap > div > div.sub_tab._tab_root > div > ul > li:nth-child(2)')  # 내일 탭
# TRS_FINE_DUST_TOMORROW = (By.CSS_SELECTOR,
#                           '#main_pack > section.sc_new._atmospheric_environment > div > div.api_cs_wrap > div > div:nth-child(4) > div.main_box > div.detail_box.list3 > div.tb_scroll > table > tbody > tr')  # 내일 미세먼지 rows
# SPAN_MICRO_FINE_DUST_TAB = (By.CSS_SELECTOR,
#                             '#main_pack > section.sc_new._atmospheric_environment > div > div.api_cs_wrap > div > div.main_tab.tab5 > ul > li:nth-child(2) > a > span')  # 초미세먼지 탭
# TRS_MICRO_FINE_DUST_TODAY = (By.CSS_SELECTOR,
#                              '#main_pack > section.sc_new._atmospheric_environment > div > div.api_cs_wrap > div > div:nth-child(3) > div.main_box > div.detail_box > div.tb_scroll > table > tbody > tr')  # 현재 초미세먼지 rows
# TRS_MICRO_FINE_DUST_TOMORROW = (By.CSS_SELECTOR,
#                                 '#main_pack > section.sc_new._atmospheric_environment > div > div.api_cs_wrap > div > div:nth-child(4) > div.main_box > div.detail_box.list3 > div.tb_scroll > table > tbody > tr')  # 내일 초미세먼지 rows
#
# """ 크롬 옵션 세팅 """
# options = webdriver.ChromeOptions()
# # 크롬브라우저 띄우지 않고 백그라운드에서 실행
# options.add_argument('headless')
# # 디바이스 어댑터 실패 로그 지우기
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
#
# """ 크롬 세팅 """
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
#
# """ 브라우저 크기 최대화 """
# driver.maximize_window()
#
# """ wait 세팅 """
# wait5 = WebDriverWait(driver, 5)
# wait10 = WebDriverWait(driver, 10)
#
# """ 브라우저 오픈 """
# driver.get(URL)
#
# """ 검색창 대기 """
# input_search = wait5.until(EC.presence_of_element_located(INPUT_SEARCH))
#
# """ 검색창 입력 """
# driver.execute_script("arguments[0].value = '" + search_keyword + "';", input_search)
#
# """ 검색버튼 대기 """
# button_search = wait5.until(EC.presence_of_element_located(BUTTON_SEARCH))
#
# """ 검색버튼 클릭 """
# driver.execute_script("arguments[0].click();", button_search)
#
# """ 오늘 미세먼지 """
# trs_fine_dust_today = wait5.until(EC.presence_of_all_elements_located(TRS_FINE_DUST_TODAY))
#
# """ tr개수만큼 반복 """
# for index, component in enumerate(trs_fine_dust_today):
#     # 관측지점
#     th_location = component.find_element(By.TAG_NAME, 'th')
#     fine_dust_info_dict_today['location'] = th_location.text
#
#     # 현재
#     span_current = component.find_element(By.CSS_SELECTOR, 'td:nth-child(2) > span')
#     fine_dust_info_dict_today['current'] = span_current.text
#
#     # 오전예보
#     span_morning = component.find_element(By.CSS_SELECTOR, 'td:nth-child(3) > span')
#     fine_dust_info_dict_today['morning'] = span_morning.text
#
#     # 오후예보
#     span_afternoon = component.find_element(By.CSS_SELECTOR, 'td:nth-child(4) > span')
#     fine_dust_info_dict_today['afternoon'] = span_afternoon.text
#
#     # 리스트에 저장
#     fine_dust_info_list_today.append(fine_dust_info_dict_today)
#
#     # 딕셔너리 복사해서 다음에 값 덮어쓸때 리스트에 들어간 딕셔너리 값까지 바뀌지 않도록
#     fine_dust_info_dict_today = fine_dust_info_dict_today.copy()
#
# """ '내일' 탭 클릭 """
# driver.find_element(*LI_TOMORROW).click()
#
# """ 내일 미세먼지 """
# trs_fine_dust_tomorrow = wait5.until(EC.presence_of_all_elements_located(TRS_FINE_DUST_TOMORROW))
#
# """ tr개수만큼 반복 """
# for index, component in enumerate(trs_fine_dust_tomorrow):
#     # 관측지점
#     th_location = component.find_element(By.TAG_NAME, 'th')
#     fine_dust_info_dict_tomorrow['location'] = th_location.text
#
#     # 오전예보
#     span_morning = component.find_element(By.CSS_SELECTOR, 'td:nth-child(2) > span')
#     fine_dust_info_dict_tomorrow['morning'] = span_morning.text
#
#     # 오후예보
#     span_afternoon = component.find_element(By.CSS_SELECTOR, 'td:nth-child(3) > span')
#     fine_dust_info_dict_tomorrow['afternoon'] = span_afternoon.text
#
#     # 리스트에 저장
#     fine_dust_info_list_tomorrow.append(fine_dust_info_dict_tomorrow)
#
#     # 딕셔너리 복사해서 다음에 값 덮어쓸때 리스트에 들어간 딕셔너리 값까지 바뀌지 않도록
#     fine_dust_info_dict_tomorrow = fine_dust_info_dict_tomorrow.copy()
#
# """ 초미세먼지 페이지로 이동 """
# driver.find_element(*SPAN_MICRO_FINE_DUST_TAB).click()
#
# """ 오늘 초미세먼지 """
# trs_micro_fine_dust_today = wait5.until(EC.presence_of_all_elements_located(TRS_MICRO_FINE_DUST_TODAY))
#
# """ tr개수만큼 반복 """
# for index, component in enumerate(trs_micro_fine_dust_today):
#     # 관측지점
#     th_location = component.find_element(By.TAG_NAME, 'th')
#     micro_fine_dust_info_dict_today['location'] = th_location.text
#
#     # 현재
#     span_current = component.find_element(By.CSS_SELECTOR, 'td:nth-child(2) > span')
#     micro_fine_dust_info_dict_today['current'] = span_current.text
#
#     # 오전예보
#     span_morning = component.find_element(By.CSS_SELECTOR, 'td:nth-child(3) > span')
#     micro_fine_dust_info_dict_today['morning'] = span_morning.text
#
#     # 오후예보
#     span_afternoon = component.find_element(By.CSS_SELECTOR, 'td:nth-child(4) > span')
#     micro_fine_dust_info_dict_today['afternoon'] = span_afternoon.text
#
#     # 리스트에 저장
#     micro_fine_dust_info_list_today.append(micro_fine_dust_info_dict_today)
#
#     # 딕셔너리 복사해서 다음에 값 덮어쓸때 리스트에 들어간 딕셔너리 값까지 바뀌지 않도록
#     micro_fine_dust_info_dict_today = micro_fine_dust_info_dict_today.copy()
#
# """ '내일' 탭 클릭 """
# driver.find_element(*LI_TOMORROW).click()
#
# """ 내일 초미세먼지 """
# trs_micro_fine_dust_tomorrow = wait5.until(EC.presence_of_all_elements_located(TRS_MICRO_FINE_DUST_TOMORROW))
#
# """ tr개수만큼 반복 """
# for index, component in enumerate(trs_micro_fine_dust_tomorrow):
#     # 관측지점
#     th_location = component.find_element(By.TAG_NAME, 'th')
#     micro_fine_dust_info_dict_tomorrow['location'] = th_location.text
#
#     # 오전예보
#     span_morning = component.find_element(By.CSS_SELECTOR, 'td:nth-child(2) > span')
#     micro_fine_dust_info_dict_tomorrow['morning'] = span_morning.text
#
#     # 오후예보
#     span_afternoon = component.find_element(By.CSS_SELECTOR, 'td:nth-child(3) > span')
#     micro_fine_dust_info_dict_tomorrow['afternoon'] = span_afternoon.text
#
#     # 리스트에 저장
#     micro_fine_dust_info_list_tomorrow.append(micro_fine_dust_info_dict_tomorrow)
#
#     # 딕셔너리 복사해서 다음에 값 덮어쓸때 리스트에 들어간 딕셔너리 값까지 바뀌지 않도록
#     micro_fine_dust_info_dict_tomorrow = micro_fine_dust_info_dict_tomorrow.copy()
#
# """ 브라우저 타이틀, url 저장 """
# window_title = driver.title
# window_url = driver.current_url
#
# """ 출력 """
# print("\n현재시간 ▶ " + str(time.strftime('%Y-%m-%d %H:%M:%S')))
#
# print("\n기준 ▶ 미세먼지 (좋음 0~30 보통~80 나쁨~150 매우나쁨151~)")
# print("오늘 ▶")
# for index, component in enumerate(fine_dust_info_list_today):
#     print('\t지역: {:6} 현재농도: {:6} 오전: {:10} 오후: {:10}'.format(component['location'], component['current'],
#                                                              component['morning'], component['afternoon']))
#
# print("내일 ▶")
# for index, component in enumerate(fine_dust_info_list_tomorrow):
#     print('\t지역: {:6} 오전: {:10} 오후: {:10}'.format(component['location'], component['morning'], component['afternoon']))
#
# print("\n기준 ▶ 초미세먼지 (좋음 0~15 보통~35 한때나쁨 나쁨~75 매우나쁨76~)")
# print("오늘 ▶")
# for index, component in enumerate(micro_fine_dust_info_list_today):
#     print('\t지역: {:6} 현재농도: {:6} 오전: {:10} 오후: {:10}'.format(component['location'], component['current'],
#                                                              component['morning'], component['afternoon']))
#
# print("내일 ▶")
# for index, component in enumerate(micro_fine_dust_info_list_tomorrow):
#     print('\t지역: {:6} 오전: {:10} 오후: {:10}'.format(component['location'], component['morning'], component['afternoon']))
#
# print("\n출처 ▶ " + window_title + "(" + window_url + ")")
#
# print("\nCreated by Numong")
#
# """ 크롬드라이버 종료 """
# driver.quit()
# # kill_chrome_driver_process()
# time.sleep(3600)
# ◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ 20210331 셀레니움 미세먼지 테스트 종료 ◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆


# ◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ 20210401 셀레니움 상영영화정보 테스트 시작 ◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆

""" 변수 """
# 영화진흥위원회 키
KOFIC_KEY = 'ba4bcd991407f6c2f27ec9244f5f9df7'
# 조회일자
print("조회일자를 20210101 형태로 입력해주세요: ", end="")
KOFIC_SEARCH_DATE = input()

# 오픈할 URL
URL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={0}&targetDt={1}'.format(KOFIC_KEY, KOFIC_SEARCH_DATE)
# 대기시간
SLEEP_SEC = 5

""" 크롬 옵션 세팅 """
options = webdriver.ChromeOptions()
# 크롬브라우저 띄우지 않고 백그라운드에서 실행
# options.add_argument('headless')
# 디바이스 어댑터 실패 로그 지우기
options.add_experimental_option('excludeSwitches', ['enable-logging'])

""" 크롬 세팅 """
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

""" 브라우저 크기 최대화 """
driver.maximize_window()

""" wait 세팅 """
wait5 = WebDriverWait(driver, 5)
wait10 = WebDriverWait(driver, 10)

""" 브라우저 오픈 """
driver.get(URL)

# ◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ 20210401 셀레니움 상영영화정보 테스트 종료 ◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆
