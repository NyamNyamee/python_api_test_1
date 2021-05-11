import logging
import os
from logging.handlers import TimedRotatingFileHandler

# 로그파일이 저장될 경로 지정
log_dir = 'C:/logs/python_test'
# log_dir = './logs'

# 로그파일이 저장될 경로가 없다면 생성
if not (os.path.isdir(log_dir)):
    os.makedirs(os.path.join(log_dir))

# 로그객체 생성
logger = logging.getLogger(__name__)
# 로그레벨 지정
logger.setLevel(logging.DEBUG)

# 로그포맷객체 생성
common_formatter = logging.Formatter('%(asctime)s [%(levelname)8s] %(message)s')

# 파일핸들러 생성
# fileHandler = TimedRotatingFileHandler(filename='C:/hanul_hbcnc_wetax/logs/hbcncRegApply.log', when='midnight', interval=1, encoding='utf-8')
# fileHandler = TimedRotatingFileHandler(filename='./logs/hbcncRegApply.log', when='midnight', interval=1, encoding='utf-8')
fileHandler = TimedRotatingFileHandler(filename='C:/logs/python_test/test.log', when='midnight', interval=1, encoding='utf-8')
# 파일핸들러 포맷 지정
fileHandler.setFormatter(common_formatter)
# 파일핸들러 접미사 지정
fileHandler.suffix = '%Y%m%d'
# 파일핸들러 레벨 지정
fileHandler.setLevel(logging.DEBUG)
# 로그객체에 파일핸들러 추가
logger.addHandler(fileHandler)

# 스트림핸들러 생성
streamHandler = logging.StreamHandler()
# 스트림핸들러 포맷 지정
streamHandler.setFormatter(common_formatter)
# 스트림핸들러 레벨 지정
streamHandler.setLevel(logging.DEBUG)
# 로그객체에 스트림핸들러 추가
logger.addHandler(streamHandler)
