# Function/app_ui_logger.py
import logging

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal


class LogEmitter(QObject):
    """다른 쓰레드의 로그 메시지를 GUI 쓰레드로 전달"""

    message_logged = Signal(str)


class TextBrowserLogHandler(logging.Handler):
    """로그 메시지를 Qt 시그널로 전달하는 로깅 핸들러"""

    def __init__(self, parent=None):
        """INFO 이상 로그를 전달할 Qt 시그널 객체를 초기화"""

        super().__init__(level=logging.INFO)
        self.emitter = LogEmitter(parent)

    def emit(self, record):
        """로그 레코드를 문자열로 변환해 GUI 쓰레드에 전달"""

        try:
            self.emitter.message_logged.emit(self.format(record))
        except Exception:
            self.handleError(record)


def add_text_browser_log_handler(text_browser, parent=None):
    """INFO 이상 로그를 지정한 QTextBrowser에 표시"""

    handler = TextBrowserLogHandler(parent)
    handler.setFormatter(logging.Formatter("%(message)s"))
    handler.emitter.message_logged.connect(text_browser.append)
    logging.getLogger().addHandler(handler)
    return handler


def remove_text_browser_log_handler(handler):
    """루트 로거에서 GUI 로그 핸들러를 안전하게 해제"""

    if handler is not None:
        logging.getLogger().removeHandler(handler)
        handler.close()
