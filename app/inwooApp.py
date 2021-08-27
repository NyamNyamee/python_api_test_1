import sys
import time
import sentry_sdk as sentry
import jproperties
from PyQt5.QtWidgets import *
from Classes.GUI.inwooMainWindow import InwooMainWindow

from Classes.Util.Logger import logger

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = InwooMainWindow()
        sys.exit(app.exec_())
    except Exception as e:
        print('크롤링 GUI 실행 에러' + str(e))
