import sys
from PyQt5.QtWidgets import *
from Classes.GUI.Inwoo.window.MainWindow import MainWindow

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = MainWindow()
        sys.exit(app.exec_())
    except Exception as e:
        print('Inwoo APP 실행 중 에러: ' + str(e))
