import ctypes
import time

import pandas as pd  # 가져온 채팅내용 DF로 쓸거라서
import win32api
import win32con
import win32gui
from pywinauto import clipboard  # 채팅창내용 가져오기 위해

# 카톡창 이름
# kakao_opentalk_name = '♥ 디아블로2레저렉션 대장방 ♥'
kakao_opentalk_name = '이인우'
# 체크할 커맨드
# chat_command = '계약번호'
chat_command = 'ㅋ'

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


def kakao_sendtext(chatroom_name, text):
    """ 채팅방 메시지 전송 """
    # # 핸들 _ 채팅방
    hwndMain = win32gui.FindWindow(None, chatroom_name)
    hwndEdit = win32gui.FindWindowEx(hwndMain, None, "RICHEDIT50W", None)

    win32api.SendMessage(hwndEdit, win32con.WM_SETTEXT, 0, text)
    SendReturn(hwndEdit)


def copy_chatroom(chatroom_name):
    """ 채팅방 내용 복사 """
    # # 핸들 _ 채팅방
    hwndMain = win32gui.FindWindow(None, chatroom_name)
    hwndListControl = win32gui.FindWindowEx(hwndMain, None, "EVA_VH_ListControl_Dblclk", None)

    # #조합키, 본문을 클립보드에 복사 ( ctl + c , v )
    time.sleep(0.5)
    PostKeyEx(hwndListControl, ord('A'), [w.VK_CONTROL], False)
    time.sleep(0.5)
    PostKeyEx(hwndListControl, ord('C'), [w.VK_CONTROL], False)
    time.sleep(1)
    ctext = clipboard.GetData()
    # print(ctext)
    return ctext


def PostKeyEx(hwnd, key, shift, specialkey):
    """ 조합키 """
    if IsWindow(hwnd):

        ThreadId = GetWindowThreadProcessId(hwnd, None)

        lparam = MakeLong(0, MapVirtualKeyA(key, 0))
        msg_down = w.WM_KEYDOWN
        msg_up = w.WM_KEYUP

        if specialkey:
            lparam = lparam | 0x1000000

        if len(shift) > 0:
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

        else:
            SendMessage(hwnd, msg_down, key, lparam)
            SendMessage(hwnd, msg_up, key, lparam | 0xC0000000)


def SendReturn(hwnd):
    """ 엔터키 입력 """
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    time.sleep(0.01)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)


def open_chatroom(chatroom_name):
    """ 채팅방 오픈 """
    # 채팅방 목록 검색하는 Edit (채팅방이 열려있지 않아도 전송 가능하기 위하여)
    hwndkakao = win32gui.FindWindow(None, "카카오톡")
    hwndkakao_edit1 = win32gui.FindWindowEx(hwndkakao, None, "EVA_ChildWindow", None)
    hwndkakao_edit2_1 = win32gui.FindWindowEx(hwndkakao_edit1, None, "EVA_Window", None)
    hwndkakao_edit2_2 = win32gui.FindWindowEx(hwndkakao_edit1, hwndkakao_edit2_1, "EVA_Window",
                                              None)  # ㄴ시작핸들을 첫번째 자식 핸들(친구목록) 을 줌(hwndkakao_edit2_1)
    hwndkakao_edit3 = win32gui.FindWindowEx(hwndkakao_edit2_2, None, "Edit", None)

    # # Edit에 검색 _ 입력되어있는 텍스트가 있어도 덮어쓰기됨
    win32api.SendMessage(hwndkakao_edit3, win32con.WM_SETTEXT, 0, chatroom_name)
    time.sleep(0.5)  # 안정성 위해 필요
    SendReturn(hwndkakao_edit3)
    time.sleep(0.5)


def save_last_chat():
    """ 채팅방 오픈, 마지막 채팅정보 리턴 """
    print("최초 세팅 시작")
    open_chatroom(kakao_opentalk_name)  # 채팅방 열기
    copied_chat_text = copy_chatroom(kakao_opentalk_name)  # 채팅내용 가져오기
    copied_chat_array = copied_chat_text.split('\r\n')  # \r\n 으로 스플릿 (대화내용에 개행이 포함뙨 경우 \r 때문에 스플릿 안됨)
    copied_chat_df = pd.DataFrame(copied_chat_array)  # DF 으로 바꾸기
    copied_chat_df[0] = copied_chat_df[0].str.replace('\[([\S\s]+)\] \[(오전|오후)([0-9:\s]+)\] ',
                                                      '')  # 정규식으로 이름, 시간 지우고 채팅내용만 남기기

    # 마지막 채팅의 인덱스, 채팅내용 리턴
    return copied_chat_df.index[-2], copied_chat_df.iloc[-2, 0]


# 채팅방 커멘드 체크
def check_command_chat(cls, clst):
    print("채팅방 내용을 탐색합니다")
    open_chatroom(kakao_opentalk_name)  # 채팅방 열기
    copied_chat_text = copy_chatroom(kakao_opentalk_name)  # 채팅내용 가져오기
    copied_chat_array = copied_chat_text.split('\r\n')  # \r\n 으로 스플릿 (대화내용에 개행이 포함뙨 경우 \r 때문에 스플릿 안됨)
    copied_chat_df = pd.DataFrame(copied_chat_array)  # DF 으로 바꾸기
    copied_chat_df[0] = copied_chat_df[0].str.replace('\[([\S\s]+)\] \[(오전|오후)([0-9:\s]+)\] ',
                                                      '')  # 정규식으로 이름, 시간 지우고 채팅내용만 남기기

    # 초기 세팅 시 마지막 채팅정보와 현재 시점의 마지막 채팅정보가 같을 때
    if copied_chat_df.iloc[-2, 0] == clst:
        print("새로운 채팅 없음")
        return copied_chat_df.index[-2], copied_chat_df.iloc[-2, 0]
    else:
        print("새로운 채팅 있음")
        copied_new_chat_df = copied_chat_df.iloc[cls + 1:, 0]  # 초기 세팅 시 채팅을 제외한 신규 채팅내용만 남김
        is_command_found = copied_new_chat_df[copied_new_chat_df.str.contains(chat_command)]  # 커맨드가 있는지 확인
        if 1 <= int(is_command_found.count()):
            print("-------커멘드 확인--------")
            # message = str(copied_new_chat_df).split(chat_command)[1].replace('[', '').replace(']', '')[:7]
            message = copied_chat_df.iloc[-2, 0]
            kakao_sendtext(kakao_opentalk_name, message)

            # 명령어 여러개 쓸경우 리턴값으로 각각 빼서 쓰면 될듯. 일단 테스트용으로 위에 하드코딩 해둠
            return copied_chat_df.index[-2], copied_chat_df.iloc[-2, 0]

        else:
            print("-------커멘드 미확인--------")
            return copied_chat_df.index[-2], copied_chat_df.iloc[-2, 0]


# # 네이버 실검 상위 20개, 리턴
def get_message_to_send():
    s = "계약번호가 있네요"
    return s


def main():
    last_chat_index, last_chat_text = save_last_chat()  # 초기 채팅방 열기, 마지막 채팅 정보 저장

    tryCount = 0
    while True:
        tryCount = tryCount + 1
        print("시도횟수: " + str(tryCount))
        last_chat_index, last_chat_text = check_command_chat(last_chat_index, last_chat_text)  # 커멘드 체크
        time.sleep(3)


if __name__ == '__main__':
    main()
