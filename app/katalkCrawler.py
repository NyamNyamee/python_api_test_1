import time
import win32api
import win32con
import win32gui
import ctypes
import requests
import pandas as pd
from pywinauto import clipboard
from apscheduler.schedulers.background import BackgroundScheduler

kakao_opentalk_name = '이인우'  # 열려있는 카톡방 이름
chat_command = '실검 알려줘'  # 테스트용..

PBYTE256 = ctypes.c_ubyte * 256
_user32 = ctypes.WinDLL("user32")
GetKeyboardState = _user32.GetKeyboardState
SetKeyboardState = _user32.SetKeyboardState
PostMessage = win32api.PostMessage
SendMessage = win32gui.SendMessage
FindWindow = win32gui.FindWindow
IsWindow = win32gui.IsWindow
GetCurrentThreadId = win32api.GetCurrentThreadId
GetWindowThreadProcessId = _user32.GetWindowThreadProcessId
AttachThreadInput = _user32.AttachThreadInput

MapVirtualKeyA = _user32.MapVirtualKeyA
MapVirtualKeyW = _user32.MapVirtualKeyW

MakeLong = win32api.MAKELONG
w = win32con


# 엔터
def press_enter(hwnd):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    time.sleep(0.01)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)


# 채팅방에 메시지 전송
def kakao_sendtext(chatroom_name, message):
    # 채팅방 윈도우
    window = win32gui.FindWindow(None, chatroom_name)
    # 채팅방 메시지인풋
    input = win32gui.FindWindowEx(window, None, "RICHEDIT50W", None)

    win32api.SendMessage(input, win32con.WM_SETTEXT, 0, message)
    press_enter(input)


# 채팅방 열기
def open_chatroom(chatroom_name):
    # 채팅방 목록 검색하는 Edit (채팅방이 열려있지 않아도 메시지 전송하기 위하여)
    kakao_main_window = win32gui.FindWindow(None, "카카오톡")
    kakao_child_01_window = win32gui.FindWindowEx(kakao_main_window, None, "EVA_ChildWindow", None)
    hwndkakao_edit2_1 = win32gui.FindWindowEx(kakao_child_01_window, None, "EVA_Window", None)
    hwndkakao_edit2_2 = win32gui.FindWindowEx(kakao_child_01_window, hwndkakao_edit2_1, "EVA_Window", None)
    hwndkakao_edit3 = win32gui.FindWindowEx(hwndkakao_edit2_2, None, "Edit", None)

    # Edit에 검색 _ 입력되어있는 텍스트가 있어도 덮어쓰기됨
    win32api.SendMessage(hwndkakao_edit3, win32con.WM_SETTEXT, 0, chatroom_name)
    # time.sleep(1)  # 안정성 위해 필요
    press_enter(hwndkakao_edit3)
    # time.sleep(1)


# # 채팅내용 가져오기
def copy_chatroom(chatroom_name):
    # # 핸들 _ 채팅방
    hwndMain = win32gui.FindWindow(None, chatroom_name)
    hwndListControl = win32gui.FindWindowEx(hwndMain, None, "EVA_VH_ListControl_Dblclk", None)

    # #조합키, 본문을 클립보드에 복사 ( ctl + c , v )
    PostKeyEx(hwndListControl, ord('A'), [w.VK_CONTROL], False)
    time.sleep(1)
    PostKeyEx(hwndListControl, ord('C'), [w.VK_CONTROL], False)
    ctext = clipboard.GetData()
    # print(ctext)
    return ctext


# # 채팅내용 초기 저장 _ 마지막 채팅
def chat_last_save():
    open_chatroom(kakao_opentalk_name)  # 채팅방 열기
    ttext = copy_chatroom(kakao_opentalk_name)  # 채팅내용 가져오기

    a = ttext.split('\r\n')  # \r\n 으로 스플릿 __ 대화내용 인용의 경우 \r 때문에 해당안됨
    df = pd.DataFrame(a)  # DF 으로 바꾸기

    df[0] = df[0].str.replace('\[([\S\s]+)\] \[(오전|오후)([0-9:\s]+)\] ', '')  # 정규식으로 채팅내용만 남기기

    return df.index[-2], df.iloc[-2, 0]


# # 채팅방 커멘드 체크
def chat_chek_command(cls, clst):
    open_chatroom(kakao_opentalk_name)  # 채팅방 열기
    ttext = copy_chatroom(kakao_opentalk_name)  # 채팅내용 가져오기

    a = ttext.split('\r\n')  # \r\n 으로 스플릿 __ 대화내용 인용의 경우 \r 때문에 해당안됨
    df = pd.DataFrame(a)  # DF 으로 바꾸기

    df[0] = df[0].str.replace('\[([\S\s]+)\] \[(오전|오후)([0-9:\s]+)\] ', '')  # 정규식으로 채팅내용만 남기기

    if df.iloc[-2, 0] == clst:
        print("채팅 없었음..")
        return df.index[-2], df.iloc[-2, 0]
    else:
        print("채팅 있었음")

        df1 = df.iloc[cls + 1:, 0]  # 최근 채팅내용만 남김

        found = df1[df1.str.contains(chat_command)]  # 챗 카운트

        if 1 <= int(found.count()):
            print("-------커멘드 확인!")
            p_time_ymd_hms = \
                f"{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday} / " \
                f"{time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}"
            realtimeList = naver_realtimeList()  # 네이버 실시간 검색어 상위 20개
            kakao_sendtext(kakao_opentalk_name, f"{p_time_ymd_hms}\n{realtimeList}")  # 메시지 전송, time/실검

            # 명령어 여러개 쓸경우 리턴값으로 각각 빼서 쓰면 될듯. 일단 테스트용으로 위에 하드코딩 해둠
            return df.index[-2], df.iloc[-2, 0]

        else:
            print("커멘드 미확인")
            return df.index[-2], df.iloc[-2, 0]


# 메시지 리턴
def get_message_to_send():
    message = '231'
    return message


# 스케줄러 job_1
def job_1():
    now = time.strftime('[%Y-%m-%d %H:%M:%S]')

    open_chatroom(kakao_opentalk_name)  # 채팅방 열기
    message = get_message_to_send()  # 메시지
    kakao_sendtext(kakao_opentalk_name, now + ' ' + message)  # 메시지 전송


# 조합키 쓰기 위해
def PostKeyEx(hwnd, key, shift, specialkey):
    if IsWindow(hwnd):

        ThreadId = GetWindowThreadProcessId(hwnd, None)

        lparam = MakeLong(0, MapVirtualKeyA(key, 0))
        msg_down = w.WM_KEYDOWN
        msg_up = w.WM_KEYUP

        if specialkey:
            lparam = lparam | 0x1000000

        if len(shift) > 0:  # Если есть модификаторы - используем PostMessage и AttachThreadInput
            pKeyBuffers = PBYTE256()
            pKeyBuffers_old = PBYTE256()

            SendMessage(hwnd, w.WM_ACTIVATE, w.WA_ACTIVE, 0)
            AttachThreadInput(GetCurrentThreadId(), ThreadId, True)
            GetKeyboardState(ctypes.byref(pKeyBuffers_old))

            for modkey in shift:
                if modkey == w.VK_MENU:
                    lparam = lparam | 0x20000000
                    msg_down = w.WM_SYSKEYDOWN
                    msg_up = w.WM_SYSKEYUP
                pKeyBuffers[modkey] |= 128

            SetKeyboardState(ctypes.byref(pKeyBuffers))
            time.sleep(0.01)
            PostMessage(hwnd, msg_down, key, lparam)
            time.sleep(0.01)
            PostMessage(hwnd, msg_up, key, lparam | 0xC0000000)
            time.sleep(0.01)
            SetKeyboardState(ctypes.byref(pKeyBuffers_old))
            time.sleep(0.01)
            AttachThreadInput(GetCurrentThreadId(), ThreadId, False)

        else:  # Если нету модификаторов - используем SendMessage
            SendMessage(hwnd, msg_down, key, lparam)
            SendMessage(hwnd, msg_up, key, lparam | 0xC0000000)


def main():
    """ 1 """
    # sched = BackgroundScheduler(timezone='Asia/Seoul')
    # sched.start()
    # sched.add_job(job_1, 'cron', second='*/3', id="test_1")
    #
    # count = 0
    #
    # while True:
    #     now = time.strftime('[%Y-%m-%d %H:%M:%S]')
    #     count = count + 1
    #     print(now + " 시도횟수 = " + str(count))
    #     time.sleep(3)

    """ 2 """
    # # # 핸들 _ 채팅방
    # hwndMain = win32gui.FindWindow(None, kakao_opentalk_name)
    # hwndListControl = win32gui.FindWindowEx(hwndMain, None, "EVA_VH_ListControl_Dblclk", None)
    #
    # # #조합키, 본문을 클립보드에 복사 ( ctl + A , C )
    # PostKeyEx(hwndListControl, ord('A'), [w.VK_CONTROL], False)
    # time.sleep(0.2)
    # PostKeyEx(hwndListControl, ord('C'), [w.VK_CONTROL], False)
    # ctext = clipboard.GetData()
    # print(ctext)  # 내용 확인

    """ 3 """
    # sched = BackgroundScheduler()
    # sched.start()

    cls, clst = chat_last_save()  # 초기설정 _ 마지막채팅 저장

    # # 매 분 5초마다 job_1 실행
    # sched.add_job(job_1, 'cron', second='*/5', id="test_1")

    while True:
        print("실행중.................")
        cls, clst = chat_chek_command(cls, clst)  # 커멘드 체크
        time.sleep(5)



if __name__ == '__main__':
    main()
