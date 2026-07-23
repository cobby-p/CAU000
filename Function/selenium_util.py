# Function/selenium_util.py
import logging
import os
import time

from knw_Chromedriver_manager import Chromedriver_manager
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from Service.constants import Constants

# 프로젝트 상수와 현재 모듈의 로거 초기화
constants = Constants()
logger = logging.getLogger(__name__)


def create_chrome_driver(headless=False):
    """백그라운드 실행 여부를 반영하여 Chrome WebDriver 생성"""

    # Chrome 실행 옵션 객체 생성
    chrome_options = Options()

    # ChromeDriver의 불필요한 자동화 관련 콘솔 로그 출력 제외
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # 웹 페이지의 오디오가 자동으로 재생되어도 소리가 출력되지 않도록 설정
    chrome_options.add_argument("--mute-audio")

    # Chrome과 웹 페이지에서 사용하는 기본 언어를 한국어로 설정
    chrome_options.add_argument("--lang=ko-KR")

    # 웹사이트의 브라우저 알림 권한 요청과 알림 표시를 차단
    chrome_options.add_argument("--disable-notifications")

    # DOM 접근이 가능해지면 페이지 이동 완료로 처리
    chrome_options.page_load_strategy = "eager"

    # Chrome 창의 크기를 1920x1080으로 고정
    chrome_options.add_argument("--window-size=1920,1080")

    # UI에서 백그라운드 실행을 선택한 경우 Chrome 창을 표시하지 않음
    if headless:
        chrome_options.add_argument("--headless=new")

    # 설치된 Chrome 버전에 맞는 ChromeDriver 경로 확인
    driver_path = Chromedriver_manager.install()

    # 설치 결과가 없거나 실제 실행 파일이 존재하지 않으면 즉시 중단
    if not driver_path or not os.path.isfile(driver_path):
        raise FileNotFoundError(
            f"ChromeDriver 실행 파일을 찾을 수 없습니다: {driver_path}"
        )

    # Constants에 설정된 최대 횟수만큼 ChromeDriver 실행 재시도
    for attempt in range(1, constants.RETRY_COUNT + 1):
        try:
            # 확인된 실행 파일과 Chrome 옵션으로 WebDriver 생성
            driver = webdriver.Chrome(
                service=Service(executable_path=driver_path),
                options=chrome_options,
            )

            # 페이지 로딩이 끝나지 않을 경우 30초 후 예외 발생
            driver.set_page_load_timeout(30)

            # 백그라운드 실행 여부를 로그에 표시할 문자열로 변환
            if headless:
                background_status = "사용"
            else:
                background_status = "미사용"

            logger.info(
                f"Chrome WebDriver 실행 완료 (백그라운드 실행: {background_status})"
            )

            return driver
        except WebDriverException:
            if attempt == constants.RETRY_COUNT:
                logger.exception(
                    "Chrome WebDriver 실행에 %d회 실패했습니다.",
                    constants.RETRY_COUNT,
                )
                raise

            # 재시도가 남아 있으면 현재 횟수와 다음 대기 시간을 로그에 기록
            logger.warning(
                "Chrome WebDriver 실행 실패 (%d/%d). %d초 후 재시도합니다.",
                attempt,
                constants.RETRY_COUNT,
                constants.RETRY_DELAY,
            )

            # ChromeDriver를 다시 실행하기 전에 설정된 시간만큼 대기
            time.sleep(constants.RETRY_DELAY)

    raise RuntimeError("Chrome WebDriver를 실행하지 못했습니다.")


def close_chrome_driver(driver):
    """생성된 Chrome WebDriver 종료"""

    # 생성된 드라이버가 없으면 종료 작업을 수행하지 않음
    if driver is None:
        return

    try:
        # Chrome 창과 연결된 ChromeDriver 프로세스를 함께 종료
        driver.quit()

        # 정상 종료 결과를 디버그 로그에 기록
        logger.info("Chrome WebDriver 종료 완료")
    except WebDriverException:
        # 종료 실패를 숨기지 않고 스택 정보와 함께 로그에 기록
        logger.exception("Chrome WebDriver 종료 중 오류가 발생했습니다.")
