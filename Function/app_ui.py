# Function/app_ui.py
import logging
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QVBoxLayout

from Service.constants import Constants

constants = Constants()
logger = logging.getLogger(__name__)
PROJECT_DIR = Path(__file__).resolve().parent.parent

_DIALOG_STYLE = """
    QDialog {
        background-color: transparent;
        font-family: "Malgun Gothic";
        font-size: 9pt;
    }
    QFrame#dialogCard {
        background-color: rgb(255, 255, 255);
        border: 1px solid rgb(210, 210, 210);
        border-radius: 6px;
    }
    QLabel#dialogTitle {
        color: rgb(25, 28, 33);
        font-size: 15px;
        font-weight: 600;
        background-color: transparent;
        border: none;
    }
    QLabel#dialogMessage {
        color: rgb(70, 70, 75);
        font-size: 13px;
        background-color: transparent;
        border: none;
    }
    QPushButton {
        min-height: 32px;
        border-radius: 6px;
        font-size: 13px;
    }
    QPushButton#acknowledgeButton {
        color: rgb(255, 255, 255);
        background-color: rgb(0, 123, 255);
        border: 1px solid rgb(0, 110, 230);
        border-radius: 6px;
    }
    QPushButton#acknowledgeButton:hover {
        background-color: rgb(0, 133, 255);
    }
    QPushButton#acknowledgeButton:pressed {
        background-color: rgb(0, 113, 235);
    }
    QPushButton#confirmButton {
        color: rgb(255, 255, 255);
        background-color: rgb(108, 117, 125);
        border: 1px solid rgb(90, 98, 104);
        border-radius: 6px;
    }
    QPushButton#confirmButton:hover {
        background-color: rgb(118, 127, 135);
    }
    QPushButton#confirmButton:pressed {
        background-color: rgb(98, 107, 115);
    }
    QPushButton#cancelButton {
        color: rgb(25, 28, 33);
        background-color: rgb(232, 232, 232);
        border: none;
    }
    QPushButton#cancelButton:hover {
        background-color: rgb(222, 222, 222);
    }
    QPushButton#cancelButton:default {
        border: none;
    }
"""


def resource_path(*path_parts):
    """개발 및 PyInstaller 패키징 환경에 맞는 리소스 절대 경로 반환"""

    base_path = Path(getattr(sys, "_MEIPASS", PROJECT_DIR))
    return base_path.joinpath(*path_parts)


def get_icon_path():
    """현재 운영체제에 맞는 애플리케이션 아이콘 경로 반환"""

    if sys.platform == "darwin":
        icon_file = "icon.icns"
    elif sys.platform == "win32":
        icon_file = "icon.ico"
    else:
        raise RuntimeError(
            f"지원하지 않는 운영체제입니다. platform={sys.platform}"
        )

    return str(resource_path("Resource", icon_file))


def get_platform_name():
    """현재 실행 중인 운영체제 반환"""

    if sys.platform == "darwin":
        return "macOS"
    elif sys.platform == "win32":
        return "Windows"
    else:
        raise RuntimeError(
            f"지원하지 않는 운영체제입니다. platform={sys.platform}"
        )


def create_dialog(parent, height):
    """공통 스타일과 크기가 적용된 모달 다이얼로그 생성"""

    dialog = QDialog(parent)
    dialog.setWindowTitle("확인")
    dialog.setWindowIcon(QIcon(get_icon_path()))
    dialog.setModal(True)
    dialog.setWindowFlag(Qt.WindowType.Dialog)
    dialog.setWindowFlag(Qt.WindowType.FramelessWindowHint)
    dialog.setWindowFlag(Qt.WindowType.NoDropShadowWindowHint)
    dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    dialog.setFixedSize(320, height)
    dialog.setStyleSheet(_DIALOG_STYLE)
    return dialog


# [GUI 로드] --------------------------------------------------------------------
def get_form_class():
    """현재 운영체제에 맞게 사전 변환된 GUI 클래스를 반환"""

    if sys.platform == "darwin":
        from Resource.main_macos_ui import Ui_MainWindow
    elif sys.platform == "win32":
        from Resource.main_windows_ui import Ui_MainWindow
    else:
        raise RuntimeError(
            f"지원하지 않는 운영체제입니다. platform={sys.platform}"
        )

    return Ui_MainWindow


def setup_main_window(window, process_name):
    """플랫폼별 UI를 로드하고 메인 윈도우의 제목과 아이콘 설정"""

    logger.debug(f"GUI 플랫폼 : {get_platform_name()}")

    form_class = get_form_class()
    ui = form_class()
    ui.setupUi(window)
    window.setWindowTitle(process_name)
    window.setWindowIcon(QIcon(get_icon_path()))
    return ui


# [메시지 박스] -----------------------------------------------------------------
def message_box(message_type, parent=None):
    """메시지 유형에 맞는 계정 안내, 작업 완료, 종료 확인 다이얼로그 표시"""

    if message_type == "emptyAccount":
        dialog = create_dialog(parent, 290)

        card = QFrame()
        card.setObjectName("dialogCard")

        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setPixmap(QIcon(get_icon_path()).pixmap(54, 54))

        title_label = QLabel("계정이 입력되지 않았습니다.")
        title_label.setObjectName("dialogTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        message_label = QLabel("ID와 PW를 모두 입력해 주세요.")
        message_label.setObjectName("dialogMessage")
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        acknowledge_button = QPushButton("확인")
        acknowledge_button.setObjectName("acknowledgeButton")
        acknowledge_button.setFixedHeight(34)
        acknowledge_button.setDefault(True)
        acknowledge_button.setFocus()

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 24, 20, 20)
        card_layout.setSpacing(10)
        card_layout.addWidget(icon_label)
        card_layout.addSpacing(8)
        card_layout.addWidget(title_label)
        card_layout.addWidget(message_label)
        card_layout.addSpacing(10)
        card_layout.addWidget(acknowledge_button)

        dialog_layout = QVBoxLayout(dialog)
        dialog_layout.setContentsMargins(16, 12, 16, 20)
        dialog_layout.addWidget(card)

        acknowledge_button.clicked.connect(dialog.accept)
        dialog.exec()

    elif message_type == "completed":
        dialog = create_dialog(parent, 290)
        dialog.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

        card = QFrame()
        card.setObjectName("dialogCard")

        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setPixmap(QIcon(get_icon_path()).pixmap(54, 54))

        title_label = QLabel("작업이 완료되었습니다.")
        title_label.setObjectName("dialogTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        message_label = QLabel(
            f"'{constants.PROCESS_NAME}' 작업이 정상적으로 완료되었습니다."
        )
        message_label.setObjectName("dialogMessage")
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        acknowledge_button = QPushButton("확인")
        acknowledge_button.setObjectName("acknowledgeButton")
        acknowledge_button.setFixedHeight(34)
        acknowledge_button.setDefault(True)
        acknowledge_button.setFocus()

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 24, 20, 20)
        card_layout.setSpacing(10)
        card_layout.addWidget(icon_label)
        card_layout.addSpacing(8)
        card_layout.addWidget(title_label)
        card_layout.addWidget(message_label)
        card_layout.addSpacing(10)
        card_layout.addWidget(acknowledge_button)

        dialog_layout = QVBoxLayout(dialog)
        dialog_layout.setContentsMargins(16, 12, 16, 20)
        dialog_layout.addWidget(card)

        acknowledge_button.clicked.connect(dialog.accept)
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()
        dialog.exec()

    elif message_type == "exit":
        dialog = create_dialog(parent, 330)

        card = QFrame()
        card.setObjectName("dialogCard")

        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setPixmap(QIcon(get_icon_path()).pixmap(54, 54))

        title_label = QLabel("이 프로그램을 종료하시겠습니까?")
        title_label.setObjectName("dialogTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        message_label = QLabel(
            f"'{constants.PROCESS_NAME}'을 종료하시겠습니까?"
        )
        message_label.setObjectName("dialogMessage")
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        confirm_button = QPushButton("종료")
        cancel_button = QPushButton("취소")
        confirm_button.setObjectName("confirmButton")
        cancel_button.setObjectName("cancelButton")
        confirm_button.setFixedHeight(34)
        cancel_button.setFixedHeight(34)
        confirm_button.setAutoDefault(False)
        cancel_button.setDefault(True)
        cancel_button.setFocus()

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 24, 20, 20)
        card_layout.setSpacing(10)
        card_layout.addWidget(icon_label)
        card_layout.addSpacing(8)
        card_layout.addWidget(title_label)
        card_layout.addWidget(message_label)
        card_layout.addSpacing(10)
        card_layout.addWidget(confirm_button)
        card_layout.addWidget(cancel_button)

        dialog_layout = QVBoxLayout(dialog)
        dialog_layout.setContentsMargins(16, 12, 16, 20)
        dialog_layout.addWidget(card)

        confirm_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            return QMessageBox.StandardButton.Yes
        return QMessageBox.StandardButton.No
    else:
        QMessageBox.critical(parent, "error", message_type)
    return None
