import time
import autoit

# # 메모장 실행
# autoit.run("notepad.exe")
# # 메모장 실행 대기
# autoit.win_wait_active("[CLASS:Notepad]", 3)
# # 메모장에 문자열 입력
# autoit.control_send("[CLASS:Notepad]", "Edit1", "hello world{!}")
# time.sleep(2)
# # 메모장 종료
# autoit.win_close("[CLASS:Notepad]")
# time.sleep(2)
# # 저장안함 버튼 클릭
# autoit.control_click("[Class:#32770]", "Button2")

# # 대법원 스캔프로그램 대기
# autoit.win_wait(title="iFormScan", timeout=15)
#
# # 이관증명서 라디오버튼 클릭
# autoit.win_wait_active(title="iFormScan", text="이관증명서", timeout=15)
# autoit.control_click(title="iFormScan", text="이관증명서", control="[NAME:Lab_ScanDocList]")
#
# # 파일가져오기 버튼 클릭
# autoit.win_wait_active(title="iFormScan", text="파일가져오기", timeout=15)
# autoit.control_click(title="iFormScan", text="파일가져오기", control="[NAME:Btn_FileOpen]")
# autoit.win_wait(title="로컬 파일 선택", timeout=15)
#
# # 파일가져오기 파일이름 입력
# autoit.win_wait_active(title="로컬 파일 선택", text="", control="[CLASS:Edit; INSTANCE:1]", timeout=15)
# autoit.control_set_text(title="로컬 파일 선택", text="", control="[CLASS:Edit; INSTANCE:1]", control_text='C:\\Users\\user\\Downloads\\이관증명서_20210329_173952578.jpg')
# autoit.control_click(title="로컬 파일 선택", text="열기(&O)", control="[CLASS:Button; INSTANCE:1]")
#
# # 대법원 스캔프로그램 대기
# autoit.win_wait(title="iFormScan", timeout=15)
#
# # 저장 버튼 클릭
# autoit.win_wait_active(title="iFormScan", text="저장", timeout=15)
# autoit.control_click(title="iFormScan", text="저장", control="[NAME:Btn_f_SaveAttach]")
#
# # 알림창에서 확인 버튼 클릭
# autoit.win_wait_active(title="", text="확인", timeout=15)
# autoit.control_click(title="", text="확인", control="[CLASS:Button; INSTANCE:1]")


# C:\Users\user\Downloads\이관증명서_20210329_173952578.jpg

# // 위임장인 경우 '등기필수령 승인' 체크해야 함
#         if (attachmentType == AttachmentType.DELEGATION_LETTER) {
#             autoItX.winWait("iFormScan", "등기필수령 승인", 30);
#             autoItX.controlClick("iFormScan", "등기필수령 승인", "[NAME:cBox_Check]");
#             autoItX.winWait("", "확인", 30);
#             autoItX.controlClick("", "확인", "[CLASS:Button; INSTANCE:1]");
#         }
#
# autoItX.winWait("iFormScan", "저장", 30);
# autoItX.controlClick("iFormScan", "저장", "[NAME:Btn_f_SaveAttach]");
#
# autoItX.winWait("", "확인", 30);
# autoItX.controlClick("", "확인", "[CLASS:Button; INSTANCE:1]");
