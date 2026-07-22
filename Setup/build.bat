set PROJECT_NAME=main_windows
set PYTHONUTF8=1
set SIGNTOOL_PATH="Setup/signtool.exe"
set CERT_PATH="Setup/mycert.pfx"
set TIMESTAMP_SERVER=http://timestamp.digicert.com
set EXEC_NAME="dist/CAU000.exe"

REM INSTALL
::pyinstaller %PROJECT_NAME%.spec

REM PYARMOR
pyarmor gen --pack %PROJECT_NAME%.spec -r main.py Common/ Function/ Service/ Resource/

::REM PFX CODESIGN
::%SIGNTOOL_PATH% sign /f %CERT_PATH% /p %CERT_PASSWORD% /tr %TIMESTAMP_SERVER% /td sha256 /as /fd sha256 %EXEC_NAME%

::REM VERIFY
::%SIGNTOOL_PATH% verify /pa /v %EXEC_NAME%
