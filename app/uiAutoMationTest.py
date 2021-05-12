import subprocess
import sys
import uiautomation as auto

# 계산기 실행
# subprocess.Popen('calc.exe')
# 컨트롤 찾기
# controller = auto.WindowControl(searchDepth=1, Name='계산기')
controller = auto.PaneControl(searchDepth=1, Name='작업 표시줄')
# 3초간 1초마다 찾았는지 확인
if not controller.Exists(3, 1):
    print('Can not find controller')
    sys.exit(0)
# 컨트롤의 버튼1 클릭
# controller.ButtonControl(Name='1').Click()
controller.ButtonControl(Name='시작').Click()
auto.ButtonControl(searchDepth=5, Name='무엇이든 찾아보세요').Click()
auto.ListItemControl(searchDepth=10, Name='캡처 도구, 앱').Click()
capture_tool_controller = auto.WindowControl(searchDepth=10, Name='캡처 도구')
capture_tool_controller.ButtonControl(Name='새로 만들기(N)').Click()


# scan_program = auto.WindowControl(searchDepth=50, Name='시스템')
# if not scan_program.Exists(3, 1):
#     print('대법원 스캔프로그램이 나타나지 않았습니다')
#     sys.exit(1)
#
# scan_program.EditControl(Name='파일 이름(N)').SendKeys(text='gaga')
