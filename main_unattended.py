# 하위 프로세스 및 패키지 참조 -----------------------------------------------------
import os
import sys
import traceback
import logging
from Common.email_sender import EmailSender
from Function.app_logger import configure_logging
from Service.constants import Constants


# 전역변수 ----------------------------------------------------------------------
try:
    os.chdir(sys._MEIPASS)
except:
    os.chdir(os.getcwd())

# 프로그램 실행 폴더
if getattr(sys, 'frozen', False):
    program_dir = os.path.dirname(os.path.abspath(sys.executable))
else:
    program_dir = os.path.dirname(os.path.abspath(__file__))

# 클래스 초기화
constants = Constants() # 상수 모듈
log_file = configure_logging(program_dir, constants.PROCESS_NAME) # 로그파일경로
logger = logging.getLogger(__name__)
email = EmailSender() # 메일 모듈

# 변수 초기화
developer = ['ca.unit@knworks.co.kr'] # 개발자 이메일주소
# -----------------------------------------------------------------------------

# main ------------------------------------------------------------------------
def main():
    try:
        logger.info(f'▷ [{constants.PROCESS_NAME}] 시작')

        # 프로세스 --------------------------------------------------------------
        # 여기서부터 코드를 작성하세요.
        # ---------------------------------------------------------------------

        logger.info(f'□ [{constants.PROCESS_NAME}] 종료')

        # 작업 완료 후 로그 발송
        email.send_email(mail_subject=f'[{constants.PROCESS_ID}] {constants.PROCESS_NAME}, [완료]', mail_body='',
                         mail_to=developer, mail_attachments=[log_file])

    except Exception as e:
        logger.error(f'※ [{constants.PROCESS_NAME}] 중 오류 : ' + traceback.format_exc())

        # 작업 실패 시 로그 발송
        email.send_email(mail_subject=f'[{constants.PROCESS_ID}] {constants.PROCESS_NAME}, [실패]', mail_body='',
                         mail_to=developer, mail_attachments=[log_file])

if __name__ == "__main__":
    main()
# -----------------------------------------------------------------------------
