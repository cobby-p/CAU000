# 🚀 RPA (CAU000)

## 📌 개요
#### - 업무 코드 : CAU000
#### - 업무 내용 : RPA

## 🔗 관련 링크
#### - [기획 아지트](https://knw.agit.in)
#### - [개발 아지트](https://knw.agit.in)
#### - [GitHub Repository](https://github.com/cobby-p/CAU000)

## 🔗 운영 도구
#### - [DAUM](https://www.daum.net)

## ✨ 업데이트
|     날짜     | 버전  | 내용 | 참고 |
|:----------:|:---:|:---|:---|
| 0000-00-00 | 1.0 | 내용 | [agit](https://knw.agit.in) |

## 🛠️ 실행 전 설정
실행 파일과 같은 경로의 `config.ini`에서 LDAP 설정

```ini
[ldap setup]
id = cobby.p
```

## 🔄 프로세스

## 📂 프로젝트 구조
```
CAU000/
├── Auth/                      # OAuth 설정 및 인증 파일
│
├── Common/                    # 설정, 메일, 로그 등 공통 모듈
│   ├── config.py              # ini 설정
│   ├── email_sender.py        # 메일 발송
│   └── log.py                 # 공통 로그
│
├── Function/                  # 애플리케이션 및 업무 유틸리티
│   ├── app_logger.py          # 실행 환경별 로깅 설정
│   ├── app_ui.py              # 플랫폼별 GUI·아이콘 경로 및 공통 GUI
│   ├── app_ui_logger.py       # QTextBrowser 로깅 설정
│   ├── file_util.py           # 파일 유틸리티
│   ├── knw_agit.py            # Agit 업무 자동화
│   └── selenium_util.py            # Chrome WebDriver 유틸리티
│
├── Resource/                  # GUI 및 애플리케이션 리소스
│   ├── checkmark.svg          # UI에서 사용하는 체크 표시 리소스
│   ├── icon.icns              # macOS 애플리케이션 아이콘
│   ├── icon.ico               # Windows 애플리케이션 아이콘
│   ├── main_macos.ui          # macOS용 Qt Designer GUI
│   └── main_windows.ui        # Windows용 Qt Designer GUI
│
├── Service/                   # 업무 전역 상수 및 서비스
│   └── constants.py           # 프로세스 정보와 앱 버전 상수
│
├── Setup/                     # UI 변환·빌드·버전 정보 설정 도구
│   ├── build.bat              # Windows PyArmor·PyInstaller 빌드 실행 스크립트
│   ├── compile_ui.py          # UI를 PySide6 모듈로 변환
│   └── version_info.rc        # Windows .exe 버전 정보
│
├── .gitignore                 # Git 무시 파일 설정
├── AGENTS.md                  # AI 에이전트 작업 지침
├── main.py                    # PySide6 GUI 실행 진입점
├── main_macos.spec            # macOS .app PyInstaller 설정
├── main_unattended.py         # 무인·스케줄러 실행 진입점
├── main_windows.spec          # Windows .exe PyInstaller 설정
├── README.md                  # 프로젝트 설명
└── requirements.txt           # Python 의존성 목록
```
