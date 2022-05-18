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


# ◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ 눈송이 ◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆

""" 변수 """
try:
    # d2r 눈송이던전 url
    url_path = input('응모할 눈송이던전 url을 입력해주세요\n')
    # d2r_snow_url_path = 'https://play.blizzard.kr/ko/diablo2/snowdungeon2'
    # 오픈할 URL
    URL = url_path
    
    """ 웹 엘리먼트 """
    DIV_GUARANTEED_ITEMS = (By.CLASS_NAME, 'label-guaranteed')  # 100% 당첨 div 리스트
    H3S_ITEM_TITLE = (By.TAG_NAME, 'h3')  # 아이템 이름이 적힌 h3 리스트
    H3S_SIBLING_OF_GUARANTEED_DIV = (By.CSS_SELECTOR, 'div.label-guaranteed + h3.title')  # 100% 당첨 div태그의 하위 형제인 h3태그
    BUTTON_SUBMIT = (By.ID, 'submit-button')  # 응모버튼
    A_FOOTER_BLIZZARD_LOGO = (By.CLASS_NAME, 'NavbarFooter-logo')  # 푸터 블리자드 로고 a태그
    # BUTTON_SUBMIT = (By.CLASS_NAME, 'gradient-button')  # 경품목록으로이동버튼
    
    """ 크롬 옵션 세팅 """
    options = webdriver.ChromeOptions()
    # 크롬브라우저 띄우지 않고 백그라운드에서 실행
    # options.add_argument('headless')
    # 디바이스 어댑터 실패 로그 지우기
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    """ 드라이버 세팅 """
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    
    """ 브라우저 크기 최대화 """
    driver.maximize_window()
    
    """ wait 세팅 """
    wait5 = WebDriverWait(driver, 5)
    wait10 = WebDriverWait(driver, 10)
    
    """ 브라우저 오픈 """
    driver.get(URL)
    
    """ 로그인, 응모 제품명 요청 """
    input('로그인 후 아무 값이나 입력해 주세요:\n')  # 로그인 확인 요청
    # product_name_to_apply = input('응모할 제품명을 정확히 입력해 주세요 ex)룬워드 집업 후디(XL):\n').strip()  # 응모 희망 제품명 입력받기

except Exception as e:
    print('엥? 예외가 발생했습니다~: ' + str(e))
    sys.exit()

""" 응모 로직 시작 """
try_count = 0
# 메뉴에 아이템이 나타날때까지 반복
while True:
    try_count += 1
    try:
        button_submit = driver.find_element(*BUTTON_SUBMIT)
        """ !!!! 아래 라인 주석 풀면 진짜 응모되니 조심 !!!! """
        button_submit.click()  # 응모버튼 클릭
        print('축하합니다! 역시 기계가 최고죠?!')
        break
    except Exception as e:
        print('아직 응모버튼이 활성화되지 않았습니다. 시도 횟수: ' + str(try_count))
        driver.refresh()

    # """ 응모 로직 시작 """
    # try_count = 0  # 시도횟수
    # is_item_presented = False  # 메뉴에 아이템이 나타났는지

    # # 메뉴에 아이템이 나타날때까지 반복
    # while not is_item_presented:
    #     # 푸터 나타날떄까지 대기
    #     wait5.until(EC.presence_of_element_located(A_FOOTER_BLIZZARD_LOGO))
    #     # 제품명 엘리먼트 찾기
    #     list_h3_sibling_of_guaranteed_div = driver.find_elements(*H3S_SIBLING_OF_GUARANTEED_DIV)
    #     # 시도횟수 증가
    #     try_count += 1
    #     # 100% 당첨보장 제품명 리스트를 돌며 작업
    #     for index, component in enumerate(list_h3_sibling_of_guaranteed_div):
    #         product_name = str(component.text).strip()  # 100% 당첨 제품명
    #         if product_name_to_apply in product_name:  # 사용자가 입력한 응모희망 제품명이 포함되어 있다면
    #             is_item_presented = True
    #
    #         if is_item_presented:  # 아이템이 나타났다면
    #             component.click()  # 컴포넌트 클릭
    #             button_submit = wait5.until(EC.presence_of_element_located(BUTTON_SUBMIT))  # 응모버튼 대기
    #             """ !!!! 아래 라인 주석 풀면 진짜 응모되니 조심 !!!! """
    #             button_submit.click()  # 응모버튼 클릭
    #             print('축하합니다! 역시 기계가 최고죠?!')
    #
    #     if not is_item_presented:  # 반복문을 다 돌아도 아이템이 나타나지 않았다면
    #         print('시도횟수: ' + str(try_count))
    #         driver.refresh()  # 새로고침
    #         continue  # while문 다시돌기

    # print('break_point')
# except Exception as e:
#     print('아쉽네요..예외가 발생했습니다: ' + str(e))

# ◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ 눈송이 ◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆
