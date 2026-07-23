# main.py
# 하위 프로세스 및 패키지 참조 ----------------------------------------------------
# import knw_license

import logging
import os
import subprocess
import sys
import time
from os import environ
from pathlib import Path

from PySide6.QtCore import QThread
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QMessageBox

from Common.config import Config
from Function.app_logger import configure_logging
from Function.app_ui import get_icon_path
from Function.app_ui import message_box
from Function.app_ui import setup_main_window
from Function.app_ui_logger import add_text_browser_log_handler
from Function.app_ui_logger import remove_text_browser_log_handler
from Function.selenium_util import close_chrome_driver
from Function.selenium_util import create_chrome_driver
from Service.constants import Constants

# 전역변수 할당 -----------------------------------------------------------------
try:
    os.chdir(getattr(sys, "_MEIPASS"))
except:
    os.chdir(os.getcwd())

# 프로그램 실행 폴더
if getattr(sys, "frozen", False):
    program_dir = os.path.dirname(os.path.abspath(sys.executable))
else:
    program_dir = os.path.dirname(os.path.abspath(__file__))

# 프로그램명 및 로깅 설정
constants = Constants()
configure_logging(program_dir, constants.PROCESS_NAME)
logger = logging.getLogger(__name__)


def compile_ui_for_development():
    """개발 환경에서 변경된 Qt Designer UI를 자동으로 변환"""
    if getattr(sys, "frozen", False):
        return

    compiler_path = Path(program_dir) / "Setup" / "compile_ui.py"
    if not compiler_path.is_file():
        raise FileNotFoundError(
            f"GUI 변환 스크립트를 찾을 수 없습니다: {compiler_path}"
        )

    subprocess.run(
        [sys.executable, str(compiler_path)],
        cwd=program_dir,
        check=True,
    )


# 작업을 별도의 쓰레드에서 처리하기 위한 클래스
class Worker(QThread):
    def __init__(self, user_id, user_pw, background=False, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.user_pw = user_pw
        self.background = background
        self.error = None

    def run(self):
        logger.info(f"[{constants.PROCESS_NAME}] 시작")
        driver = None

        try:
            driver = create_chrome_driver(headless=self.background)

            # 셀레니움 업무 로직을 이 영역에 작성하세요.
            driver.get("https://www.naver.com")

            time.sleep(10)

        except Exception as error:
            self.error = error
            logger.exception(
                f"[{constants.PROCESS_NAME}] 작업 중 오류가 발생했습니다."
            )
        finally:
            close_chrome_driver(driver)

        if self.error is None:
            logger.info(f"[{constants.PROCESS_NAME}] 종료")


class Form(QMainWindow):
    # QMainWindow 설정 및 시작 --------------------------------------------------
    def __init__(self, parent=None):
        super().__init__()

        # 클래스 초기화
        self.ui = setup_main_window(self, constants.PROCESS_NAME)
        config = Config(os.path.join(program_dir, "config.ini"))
        self.ui.lineEdit_id.setText(config.get("ldap setup", "id"))
        self.text_browser_log_handler = add_text_browser_log_handler(
            self.ui.textBrowser, self
        )

        self.ui.pushButton_start.clicked.connect(self.start)
        self.ui.pushButton_end.clicked.connect(self.close_program)

    # [시작] 클릭 --------------------------------------------------------------
    def start(self):
        # ui에서 입력받은 값 가져오기
        user_id = self.ui.lineEdit_id.text().strip()
        user_pw = self.ui.lineEdit_pw.text().strip()
        background = self.ui.checkBox_background.isChecked()

        # 계정이 입력되지 않았을 경우 예외처리
        if user_id == "" or user_pw == "":
            message_box("emptyAccount", self)
        else:
            # 작업 실행
            self.ui.pushButton_start.setEnabled(False)
            self.ui.pushButton_start.setText("실행 중...")
            self.ui.checkBox_background.setEnabled(False)
            try:
                self.worker = Worker(
                    user_id,
                    user_pw,
                    background=background,
                )
                self.worker.finished.connect(self.on_finished)
                self.worker.start()
            except Exception:
                self.ui.pushButton_start.setEnabled(True)
                self.ui.pushButton_start.setText("시작")
                self.ui.checkBox_background.setEnabled(True)
                logger.exception("작업 쓰레드 시작 중 오류가 발생했습니다.")
                raise

    # 작업 완료 후 GUI 복귀
    def on_finished(self):
        self.ui.pushButton_start.setEnabled(True)
        self.ui.pushButton_start.setText("시작")
        self.ui.checkBox_background.setEnabled(True)
        self.show()
        if self.worker.error is None:
            message_box("completed", self)
        else:
            QMessageBox.critical(
                self,
                "오류",
                "작업 중 오류가 발생했습니다. 로그를 확인해 주세요.",
            )

    # 프로그램 종료
    def close_program(self):
        self.close()

    # 프로그램 종료 시 이벤트 처리
    def closeEvent(
        self, event
    ):  # pyright: ignore[reportIncompatibleMethodOverride]
        if event is None:
            return

        reply = message_box("exit", self)
        if reply == QMessageBox.StandardButton.Yes:
            remove_text_browser_log_handler(self.text_browser_log_handler)
            self.text_browser_log_handler = None
            event.accept()
        else:
            event.ignore()


# main ------------------------------------------------------------------------
def main():
    compile_ui_for_development()
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    app.setApplicationName(constants.PROCESS_NAME)
    app.setApplicationDisplayName(constants.PROCESS_NAME)
    app.setWindowIcon(QIcon(get_icon_path()))
    form = Form()
    form.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
