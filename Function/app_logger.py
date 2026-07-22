# Function/app_logger.py
import datetime
import logging
import os
import sys
from pathlib import Path


def configure_logging(exec_dir="", process_name=""):
    """실행 환경에 맞는 로그 경로를 정하고 파일·콘솔 로깅을 설정"""

    if sys.platform == "darwin" and getattr(sys, "frozen", False) and process_name:
        log_dir = os.path.join(Path.home(), "Library", "Logs", process_name)
    elif exec_dir:
        log_dir = os.path.join(exec_dir, "Log")
    else:
        log_dir = Path(sys.argv[0]).parent / "Log"

    try:
        os.makedirs(log_dir, exist_ok=True)
    except PermissionError:
        if exec_dir:
            log_dir = os.path.join(exec_dir, "Log")
        else:
            log_dir = Path(sys.argv[0]).parent / "Log"
        os.makedirs(log_dir, exist_ok=True)

    current_date = datetime.datetime.now().strftime("%Y%m%d")
    log_file = os.path.join(log_dir, f"Log_{current_date}.log")

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    log_file_path = os.path.abspath(log_file)
    file_handler = None

    has_file_handler = any(
        isinstance(handler, logging.FileHandler)
        and os.path.abspath(handler.baseFilename) == log_file_path
        for handler in root_logger.handlers
    )
    if not has_file_handler:
        try:
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
        except PermissionError:
            if exec_dir:
                log_dir = os.path.join(exec_dir, "Log")
            else:
                log_dir = Path(sys.argv[0]).parent / "Log"
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, f"Log_{current_date}.log")
            file_handler = logging.FileHandler(log_file, encoding="utf-8")

    if file_handler:
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s - %(levelname)s - %(message)s",
                datefmt="%Y/%m/%d %H:%M",
            )
        )
        root_logger.addHandler(file_handler)

    has_console_handler = any(
        isinstance(handler, logging.StreamHandler)
        and not isinstance(handler, logging.FileHandler)
        for handler in root_logger.handlers
    )
    if not has_console_handler:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        root_logger.addHandler(console_handler)

    return log_file
