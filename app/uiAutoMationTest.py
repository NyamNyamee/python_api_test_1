import subprocess
import sys
import uiautomation as auto

# subprocess.Popen('calc.exe')
#
# calculator = auto.WindowControl(searchDepth=5, Name='계산기')
# if not calculator.Exists(3, 1):
#     print('Can not find Calculator window')
#     sys.exit(0)
#
# calculator.ButtonControl(Name="1").Click()

scan_program = auto.WindowControl(searchDepth=50, Name='시스템')
if not scan_program.Exists(3, 1):
    print('대법원 스캔프로그램이 나타나지 않았습니다')
    sys.exit(1)

scan_program.EditControl(Name='파일 이름(N)').SendKeys(text='gaga')
