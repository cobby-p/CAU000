# 패키지 Install ----------------------------------------------------------------
#
"""
package_list = [
    'webdriver-manager==3.4.2',
    'cryptography==41.0.1',
    'selenium==4.10.0',
    'pyautoit==0.6.5',
    'pyperclip==1.8.2'
]

import subprocess
subprocess.run(['pip', 'install'] + package_list, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
"""

# 패키지 Import -----------------------------------------------------------------
import time
import autoit
import pyperclip

from cryptography.fernet import Fernet

from knw_Chromedriver_manager import Chromedriver_manager

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Agit 로그인 -------------------------------------------------------------------
def login(agitGroup):
    """
    [Agit 로그인]

    :Args
       - (필수) agitGroup : 접속하려는 아지트 그룹의 Url

    :Example
       - Agit.login(agitGroup)
    """
    try:
        # Agit 계정 복호화 (dev.knwrpa1) -----------------------------------------
        encrypt_key = b'7W5x8QSoLp3kThW97WZ2_UTg59Ql8GxCytWL8Pzb_ec='
        encrypt_id = 'gAAAAABkhrMYXJZhORxEnRfvMChcMbq1eND33hJPGcnx2MMUMIOTuCYjHrbuH_H9MHZI3_szWyXPMwbsrdFn39RyzaefKAOSwQ=='
        encrypt_pw = 'gAAAAABkhrMYcZEJIi3lIC7Q266w9ZZTBh5r2tVq1WUZFkwmphy69d1KWLxhVWc7wKQo5OC24IkgYrnzUWTmvOg199DMrfqtKw=='

        cipher_suite = Fernet(encrypt_key)
        agitId = cipher_suite.decrypt(encrypt_id.encode()).decode()
        agitPw = cipher_suite.decrypt(encrypt_pw.encode()).decode()
        # ---------------------------------------------------------------------
        print('▷ [Agit Login] 시작')

        options = Options()

        #### 선택옵션 -----------------------------------------------------------
        ## chrome kill
        # os.system('taskkill /f /im chrome.exe')
        # time.sleep(2)

        ## chrome headless
        # options.add_argument('headless')

        ## chrome user data
        # user_data = fr'C:\Users\{getpass.getuser()}\AppData\Local\Google\Chrome\User Data'
        # options.add_argument(f"user-data-dir={user_data}")
        #### ------------------------------------------------------------------

        options.add_experimental_option('detach', True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--ignore-certificate-errors')
        # options.add_argument('headless')

        service = Service(Chromedriver_manager.install())
        driver = webdriver.Chrome(service=service, options=options)

        # Agit 그룹 이동
        driver.get(agitGroup)
        driver.maximize_window()
        driver.implicitly_wait(10)

        # Agit 로그인
        try:
            driver.find_element(By.XPATH, '//*[@id="j_username"]').send_keys(agitId)
            driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(agitPw)
            driver.find_element(By.XPATH, '//*[@id="loginForm"]/fieldset/fieldset[3]/input').click()

            driver.implicitly_wait(10)
            time.sleep(3)
        except Exception as e:
            driver.find_element(By.XPATH, '//input[@name="j_username"]').send_keys(agitId)
            driver.find_element(By.XPATH, '//input[@name="j_password"]').send_keys(agitPw)
            driver.find_element(By.XPATH, '//button[@class="submit-button"]').click()

            driver.implicitly_wait(10)
            time.sleep(3)

            driver.get(agitGroup)
            pass

        driver.implicitly_wait(10)
        time.sleep(3)

        print('□ [Agit Login] 종료')
        return driver
        # ---------------------------------------------------------------------
    except Exception as e:
        raise Exception('※ [Agit Login] 오류 : ' + str(e))


# Agit 새글 작성 ----------------------------------------------------------------
def post_new(*args):
    """
    [Agit 새글 작성]

    :Args
       - (필수) agitGroup : 접속하려는 아지트 그룹의 Url
       - (필수) agitTitle : 작성하려는 새글의 제목
       - (필수) agitBody :  작성하려는 새글의 본문
       - (선택) agitMention : 멘션 대상자
       - (선택) agitAttachment : 첨부파일

    :Example
       - Agit.post_new(agitGorup, agitTitle, agitBody, agitMention, agitAttachment)
       - Agit.post_new([agitGorup, agitTitle, agitBody, agitMention])
    """
    global driver

    try:
        # 입력받은 인수 할당 ------------------------------------------------------
        if type(args[0]) == list:
            agitGroup = args[0][0]
            agitTitle = args[0][1]
            agitBody = args[0][2]
            try:
                if not any('C:' in element.upper() for element in args[0][3]):
                    agitMention = args[0][3]
                    agitAttachment = args[0][4]
                else:
                    agitMention = ''
                    agitAttachment = args[0][3]
            except:
                agitMention = args[0][3]
                agitAttachment = ''
        else:
            agitGroup = args[0]
            agitTitle = args[1]
            agitBody = args[2]
            try:
                if not any('C:' in element.upper() for element in args[3]):
                    agitMention = args[3]
                    agitAttachment = args[4]
                else:
                    agitMention = ''
                    agitAttachment = args[3]
            except:
                agitMention = args[3]
                agitAttachment = ''

        # Agit 로그인 -----------------------------------------------------------
        driver = login(agitGroup)

        # 글쓰기 탭 이동 ---------------------------------------------------------
        driver.find_element(By.XPATH,'//i[@class="ico ico-wall_form_plain"]').click()

        # 본문 작성 -------------------------------------------------------------
        print('▷ [Agit Post_new] 시작')
        strBody = ''
        strSheetInfo = ''

        # 입력받은 본문 나누기 -----------------------------------------------------
        agitBodyList = agitBody.split('\n')

        # 나누어진 문자열마다 tag 붙이기 ---------------------------------------------
        for agitBodyList_idx, agitBodyList_row in enumerate(agitBodyList):
            if '구글시트' in agitBodyList_row:
                sheetName = agitBodyList_row[agitBodyList_row.index(':') + 1:agitBodyList_row.index('|')].strip()
                sheetUrl = agitBodyList_row[agitBodyList_row.index('|') + 1:].strip()
                strSheetInfo = f"<a href={sheetName} target=_blank class=ProseMirror__gdrive rel=noopener referrerpolicy=no-referrer>{sheetUrl}</a>"
                strBody = strBody + '<p>구글시트 : </p>'
                strBody = strBody + '<p>' + strSheetInfo + '</p>'
            elif agitBodyList_row == '':
                strBody = strBody + '<p><br></p>'
            else:
                strBody = strBody + '<p>' + agitBodyList_row + '</p>'

        # 최종적으로 입력 될 본문 할당 -----------------------------------------------
        if agitMention != '':
            mention = '"<p>To. </p>"'
        else:
            mention = '""'

        innerHTML = f'"<h1><strong>[RPA] {agitTitle}</strong></h1>"+' \
                    '"<p><br></p>"+' \
                    f'{mention}+' \
                    '"<p><br></p>"+' \
                    f'"<blockquote>{strBody}</blockquote>"+' \
                    '"<p><br></p>"+' \
                    '"<p>※ 본 게시글은 RPA가 작성 하였습니다.</p>"'

        # 본문 입력 -------------------------------------------------------------
        print(' ※ 본문 입력')
        driver.execute_script(f'document.querySelector("#agBody > section > div > '
                              f'div.message-form-group.message-form-group--PLAIN > div.message-form-group__body > '
                              f'div > div > div > div.message-form__text-wrap > div.react-measure-wrap > '
                              f'div.prosemirror-root-dom.ProseMirror").innerHTML={innerHTML}')
        time.sleep(2)

        # 멘션 입력 -------------------------------------------------------------
        if agitMention != '':
            print(' ※ 멘션 입력')
            # # 멘션 입력
            # Ctrl + Home으로 커서를 글 제일 상단으로 이동, 'ARROW 두번으로 'to'위치 이동, 'End'로 마지막 이동
            driver.find_element(By.XPATH, '//*[@id="agBody"]/section/div/div[2]/div[2]/div/div/div/div[1]/div[1]/div[1]').send_keys(Keys.LEFT_CONTROL + Keys.HOME)
            for count in range(2):
                driver.find_element(By.XPATH, '//*[@id="agBody"]/section/div/div[2]/div[2]/div/div/div/div[1]/div[1]/div[1]').send_keys(Keys.ARROW_DOWN)
            driver.find_element(By.XPATH, '//*[@id="agBody"]/section/div/div[2]/div[2]/div/div/div/div[1]/div[1]/div[1]').send_keys(Keys.END)

            # ldap입력 후 대기 2초 후 탭
            for mention in agitMention:
                print('  - ' + mention)
                #driver.find_element(By.XPATH, '//*[@id="agBody"]/section/div/div[2]/div[2]/div/div/div/div[1]/div[1]/div[1]').send_keys('@' + mention)
                # XPATH를 사용하여 요소 찾기
                element = driver.find_element(By.XPATH,
                                              '//*[@id="agBody"]/section/div/div[2]/div[2]/div/div/div/div[1]/div[1]/div[1]')

                # '@'를 먼저 입력
                element.send_keys('@')

                # mention 문자열을 한 글자씩 입력
                for char in mention:
                    element.send_keys(char)
                    time.sleep(0.1)  # 각 문자 입력 사이에 지연을 추가

                time.sleep(3)

                driver.find_element(By.XPATH, '//*[@id="agBody"]/section/div/div[2]/div[2]/div/div/div/div[1]/div[1]/div[1]').send_keys(Keys.TAB)

        # 첨부파일 등록 ----------------------------------------------------------
        print(' ※ 첨부파일 등록')
        if agitAttachment != '':
            for agitAttachment_idx, agitAttachment_row in enumerate(agitAttachment):
                # '파일첨부' 클릭
                driver.find_element(By.XPATH, '//span[@class="message-form__attach-file"]').click()
                autoit.win_wait_active("열기", 30)
                time.sleep(2)

                # 첨부파일 경로 입력 후 확인
                autoit.control_send("열기", "Edit1", "^a" + agitAttachment_row.replace(';', ':'))
                time.sleep(2)
                autoit.control_click("열기", "Button1")

                # 업로드 되었는지 확인
                for retry in range(1, 100):
                    try:

                        cancelMark = len(driver.find_elements(By.XPATH, '//button[@class="icon-button attachments-box__file-cancel-btn"]'))
                        if cancelMark == retry:
                            print(' - 업로드 완료 : ' + agitAttachment_row)
                            time.sleep(2)
                            break
                        else:
                            time.sleep(1)
                    except:
                        print(' - 첨부파일 업로드 중 : ' + str(retry) + '...')

        # 작성하기
        driver.execute_script(
            'document.querySelector("#agBody > section > div > div.message-form-group.message-form-group--PLAIN > '
            'div.message-form-group__body > div > div > div > div.message-form__footer > '
            'div.message-form-submit-control > button.ra-button.message-form-submit-control__submit-button.ra-button--accent").click()')
        time.sleep(2)


        # 멘션 리스트에 group이 있을경우 발생하는 알럿 클릭
        if 'group' in agitMention:
            driver.find_element(By.XPATH, '//html/body/div[3]/div/button[1]').click()

        print('□ [Agit Post_new] 종료')
    except Exception as e:
        raise Exception('※ [Agit Post_new] 오류 : ' + str(e))
    finally:
        # chrome 끄기
        if driver:
            driver.close()


# Agit 댓글 작성 ----------------------------------------------------------------
def post_comment(*args):
    """
    [Agit 댓글 작성]

    :Args
       - (필수) agitGroup : 접속하려는 아지트 그룹의 Url
       - (필수) agitThread : 댓글이 달릴 스레드의 제목
       - (필수) agitTitle : 작성하려는 댓글의 제목
       - (필수) agitBody :  작성하려는 댓글의 본문
       - (선택) agitMention : 멘션 대상
       - (선택) agitAttachment : 첨부파일

    :Example
       - Agit.post_comment(agitGorup, agitThread, agitTitle, agitBody, agitMention, agitAttachment)
       - Agit.post_comment([agitGorup, agitThread, agitTitle, agitBody, agitMention])
       - Agit.post_comment(agitGorup, agitThread, agitTitle, agitBody)
       - Agit.post_comment([agitGorup, agitThread, agitTitle, agitBody])
    """
    global driver

    try:
        # 입력받은 인수 할당 ------------------------------------------------------
        if type(args[0]) == list:
            agitGroup = args[0][0]
            agitThread = args[0][1]
            agitTitle = args[0][2]
            agitBody = args[0][3]
            try:
                if not any('C:' in element.upper() for element in args[0][4]):
                    agitMention = args[0][4]
                    agitAttachment = args[0][5]
                else:
                    agitMention = ''
                    agitAttachment = args[0][4]
            except:
                agitMention = args[0][4]
                agitAttachment = ''
        else:
            agitGroup = args[0]
            agitThread = args[1]
            agitTitle = args[2]
            agitBody = args[3]
            try:
                if not any('C:' in element.upper() for element in args[4]):
                    agitMention = args[4]
                    agitAttachment = args[5]
                else:
                    agitMention = ''
                    agitAttachment = args[4]
            except:
                agitMention = args[4]
                agitAttachment = ''

        # Agit 로그인 -----------------------------------------------------------
        driver = login(agitGroup)

        # 글 검색 ---------------------------------------------------------------
        driver.find_element(By.XPATH, '//*[@id="agitRoot"]/div/div/header/div/div/form/div[1]/input[2]').send_keys(agitThread + Keys.ENTER)
        driver.implicitly_wait(10)
    
        # 검색된 첫 글의 링크 가져오기
        try:
            agitThread = driver.find_element(By.XPATH, '//*[@id="agBody"]/section/div/div[3]/div[2]/div[1]/div/div/section/div[3]/a').get_attribute('href')
            driver.get(agitThread)
            driver.implicitly_wait(10)
            time.sleep(1)
        except:
            return    'noThread'

        # 본문 작성 -------------------------------------------------------------
        print('▷ [Agit Post_comment] 시작')
        strBody = ''
        strSheetInfo = ''

        # 입력받은 본문 나누기 -----------------------------------------------------
        agitBodyList = agitBody.split('\n')

        # 나누어진 문자열마다 tag 붙이기 ---------------------------------------------
        for agitBodyList_idx, agitBodyList_row in enumerate(agitBodyList):
            if '구글시트' in agitBodyList_row:
                sheetName = agitBodyList_row[agitBodyList_row.index(':') + 1:agitBodyList_row.index('|')].strip()
                sheetUrl = agitBodyList_row[agitBodyList_row.index('|') + 1:].strip()
                strSheetInfo = f"<a href={sheetName} target=_blank class=ProseMirror__gdrive rel=noopener referrerpolicy=no-referrer>{sheetUrl}</a>"
                strBody = strBody + '<p>구글시트 : </p>'
                strBody = strBody + '<p>' + strSheetInfo + '</p>'
            elif agitBodyList_row == '':
                strBody = strBody + '<p><br></p>'
            else:
                strBody = strBody + '<p>' + agitBodyList_row + '</p>'

        # 최종적으로 입력 될 본문 할당 -----------------------------------------------
        if agitMention != '':
            mention = '"<p>To. </p>"'
        else:
            mention = '""'

        innerHTML = f'"<h1><strong>[RPA] {agitTitle}</strong></h1>"+' \
                    '"<p><br></p>"+' \
                    f'{mention}+' \
                    '"<p><br></p>"+' \
                    f'"<blockquote>{strBody}</blockquote>"+' \
                    '"<p><br></p>"+' \
                    '"<p>※ 본 게시글은 RPA가 작성 하였습니다.</p>"'

        # 본문 입력 -------------------------------------------------------------
        print(' ※ 본문 입력')
        driver.find_element(By.XPATH, '//div[@class="ProseMirror__placeholder"]').click()
        driver.execute_script(f'document.querySelector("#agBody > section > div > '
                              f'div.wall__wall-thread > div.wall__wall-thread-rest-container > '
                              f'div.comment-form.comment-form--editing > div > div > div > div > '
                              f'div.message-form__text-wrap > div.react-measure-wrap > div.prosemirror-root-dom.ProseMirror").innerHTML={innerHTML}')
        time.sleep(2)


        # 멘션 입력 -------------------------------------------------------------
        print(' ※ 멘션 입력')
        if agitMention != '':
            # # 멘션 입력
            # Ctrl + Home으로 커서를 글 제일 상단으로 이동, 'ARROW 두번으로 'to'위치 이동, 'End'로 마지막 이동
            driver.find_element(By.XPATH, '//*[@id="agBody"]/section/div/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[1]/div[1]').send_keys(Keys.LEFT_CONTROL + Keys.HOME)
            for count in range(2):
                driver.find_element(By.XPATH, '//*[@id="agBody"]/section/div/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[1]/div[1]').send_keys(Keys.ARROW_DOWN)
            driver.find_element(By.XPATH, '//*[@id="agBody"]/section/div/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[1]/div[1]').send_keys(Keys.END)

            # ldap입력 후 대기 2초 후 탭
            for mention in agitMention:
                print('  - ' + mention)
                #driver.find_element(By.XPATH, '//*[@id="agBody"]/section/div/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[1]/div[1]').send_keys('@' + mention)
                # XPATH를 사용하여 요소 찾기
                element = driver.find_element(By.XPATH,
                                              '//*[@id="agBody"]/section/div/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[1]/div[1]')

                # '@'를 먼저 입력
                element.send_keys('@')

                # mention 문자열을 한 글자씩 입력
                for char in mention:
                    element.send_keys(char)
                    time.sleep(0.1)  # 각 문자 입력 사이에 지연을 추가

                time.sleep(2)
                driver.find_element(By.XPATH, '//*[@id="agBody"]/section/div/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[1]/div[1]').send_keys(Keys.TAB)


        # 첨부파일 등록 ----------------------------------------------------------
        print(' ※ 첨부파일 등록')
        if agitAttachment != '':
            for agitAttachment_idx, agitAttachment_row in enumerate(agitAttachment):
                # '파일첨부' 클릭
                driver.find_element(By.XPATH, '//span[@class="message-form__attach-file"]').click()
                autoit.win_wait_active("열기", 10)
                time.sleep(2)

                # 첨부파일 경로 입력 후 확인
                autoit.control_send("열기", "Edit1", "^a" + agitAttachment_row.replace(';', ':'))
                time.sleep(2)
                autoit.control_click("열기", "Button1")

                # 업로드 되었는지 확인
                for retry in range(1, 100):
                    try:
                        cancelMark = len(driver.find_elements(By.XPATH, '//button[@class="icon-button attachments-box__file-cancel-btn"]'))
                        if cancelMark == retry:
                            print(' - 업로드 완료 : ' + agitAttachment_row)
                            time.sleep(2)
                            break
                        else:
                            time.sleep(1)
                    except:
                        print(' - 첨부파일 업로드 중 : ' + str(retry) + '...')


        # 작성하기
        driver.execute_script(
            'document.querySelector("#agBody > section > div > div.wall__wall-thread > div.wall__wall-thread-rest-container > ' \
            'div.comment-form.comment-form--editing > div > div > div > div > div.message-form__footer > ' \
            'div.message-form-submit-control > button.ra-button.message-form-submit-control__submit-button.ra-button--accent").click()')
        time.sleep(2)

        # 멘션 리스트에 group이 있을경우 발생하는 알럿 클릭
        if 'group' in agitMention:
            driver.find_element(By.XPATH, '//html/body/div[3]/div/button[1]').click()

        print('□ [Agit Post_comment] 종료')
    except Exception as e:
        raise Exception('※ [Agit Post_comment] 오류 : ' + str(e))
    finally:
        # chrome 끄기
        if driver:
            driver.close()

# Agit 일정 작성 ----------------------------------------------------------------
def post_schedule(*args):
    """
    [Agit 일정 작성]
    ※ 주의 : 일정은 headless 불가

    :Args
       - (필수) agitGroup : 접속하려는 아지트 그룹의 Url
       - (필수) agitScheduel : 등록하려는 일정
       - (필수) agitTitle : 작성하려는 일정의 제목
       - (선택) agitBody :  작성하려는 일정의 본문
       - (선택) agitMention : 멘션 대상자

    :Example
       - Agit.post_schedule(agitGorup, agitScheduel, agitTitle, agitBody, agitMention)
       - Agit.post_schedule([agitGorup, agitScheduel, agitTitle, agitBody, agitMention])
       - Agit.post_schedule(agitGorup, agitScheduel, agitTitle)
       - Agit.post_schedule([agitGorup, agitScheduel, agitTitle])
    """
    global driver

    try:
        # 입력받은 인수 할당 ------------------------------------------------------
        if type(args[0]) == list:
            agitGroup = args[0][0]
            agitScheduel = args[0][1]
            agitTitle = args[0][2]
            try:
                agitBody = args[0][3]
            except:
                agitBody = ''
            try:
                agitMention = args[0][4]
            except:
                agitMention = ''
        else:
            agitGroup = args[0]
            agitScheduel = args[1]
            agitTitle = args[2]
            try:
                agitBody = args[3]
            except:
                agitBody = ''
            try:
                agitMention = args[4]
            except:
                agitMention = ''

        # Agit 로그인 -----------------------------------------------------------
        driver = login(agitGroup)

        print('▷ [Agit Post_schedule] 시작')
        # 일정 검색 -------------------------------------------------------------
        driver.find_element(By.XPATH, '//*[@id="agitRoot"]/div/div/header/div/div/form/div[1]/input[2]').send_keys(agitTitle + Keys.ENTER)
        driver.implicitly_wait(10)

        # 검색된 글이 있을경우 넘어가기
        try:
            originalThread = driver.find_element(By.XPATH, '//*[@id="agBody"]/section/div/div[3]/div[2]/div[1]/div/div/section/div[3]/a').get_attribute('href')
            driver.implicitly_wait(10)
            time.sleep(1)
            print('   ※ ' + agitTitle + ' 이미 일정이 존재합니다.')
        except:
            # '일정' 탭 이동 -----------------------------------------------------
            driver.get(agitGroup)
            driver.implicitly_wait(10)
            time.sleep(1)
            driver.find_element(By.XPATH, '//i[@class="ico ico-wall_form_schedule"]').click()

            # 일정 작성 ---------------------------------------------------------
            strBody = ''
            strSheetInfo = ''



            # 입력받은 일정 나누기 -------------------------------------------------
            startDate = agitScheduel.split('-')[0].split()
            endDate = agitScheduel.split('-')[1].split()
            inputDate = (endDate + startDate)

            # 일정 순서 바꾸기
            if len(inputDate) > 2:
                inputDate[1], inputDate[2] = inputDate[2], inputDate[1]

            # 입력받은 본문 나누기 -------------------------------------------------
            agitBodyList = agitBody.split('\n')

            # 나누어진 문자열마다 tag 붙이기 -----------------------------------------
            for agitBodyList_idx, agitBodyList_row in enumerate(agitBodyList):
                if '구글시트' in agitBodyList_row:
                    sheetName = agitBodyList_row[agitBodyList_row.index(':') + 1:agitBodyList_row.index('|')].strip()
                    sheetUrl = agitBodyList_row[agitBodyList_row.index('|') + 1:].strip()
                    strSheetInfo = f"<a href={sheetName} target=_blank class=ProseMirror__gdrive rel=noopener referrerpolicy=no-referrer>{sheetUrl}</a>"
                    strBody = strBody + '<p>구글시트 : </p>'
                    strBody = strBody + '<p>' + strSheetInfo + '</p>'
                elif agitBodyList_row == '':
                    strBody = strBody + '<p><br></p>'
                else:
                    strBody = strBody + '<p>' + agitBodyList_row + '</p>'

            # 최종적으로 입력 될 본문 할당 -------------------------------------------
            if agitMention != '':
                mention = '"<p>To. </p>"'
            else:
                mention = '""'

            innerHTML = '"<p><br></p>"+' \
                        f'"<blockquote>{strBody}</blockquote>"+' \
                        '"<p><br></p>"+'

            # 일정 입력 ---------------------------------------------------------
            print(' ※ 일정 입력')
            if not any(':' in element for element in inputDate):
                # 시간이 포함되어 있지 않으면 '종일' 클릭
                driver.find_elements(By.XPATH, '//input[@type="checkbox"]')[0].click()
                # datepiker 객체 가져오기 및 순서 바꾸기
                dateArea = driver.find_elements(By.XPATH, '//*[@class="react-datepicker__input-container"]')
                dateArea = dateArea[::-1]
            else:
                # datepiker 객체 가져오기 및 순서 바꾸기
                dateArea = driver.find_elements(By.XPATH, '//*[@class="react-datepicker__input-container"]')
                dateArea[1], dateArea[3], dateArea[0], dateArea[2] = dateArea[0], dateArea[1], dateArea[2], dateArea[3]

            for dateArea_idx, dateArea_row in enumerate(dateArea):
                dateArea_row.click()
                time.sleep(1)
                ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                time.sleep(1)
                ActionChains(driver).send_keys(inputDate[dateArea_idx]).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
                time.sleep(1)

            # 제목 입력 ---------------------------------------------------------
            driver.find_element(By.XPATH, '//input[@placeholder="일정 제목을 입력하세요"]').send_keys(agitTitle)

            # 멘션 입력 ---------------------------------------------------------
            if agitMention != '':
                print(' ※ 멘션 입력')
                # '참석자 지정' 클릭
                driver.find_elements(By.XPATH, '//input[@type="checkbox"]')[1].click()
                # 멘션 입력
                for mention in agitMention:
                    print('  - ' + mention)
                    driver.find_element(By.XPATH, '//input[@class="multi-value-input__input"]').send_keys('@' + mention)
                    time.sleep(2)
                    driver.find_element(By.XPATH, '//input[@class="multi-value-input__input"]').send_keys(Keys.TAB)


            # 본문 입력 ---------------------------------------------------------
            print(' ※ 본문 입력')
            if agitBody != '':
                driver.execute_script(f'document.querySelector("#agBody > section > div > '
                                      f'div.message-form-group.message-form-group--SCHEDULE > '
                                      f'div.message-form-group__body > div >  '
                                      f'div.message-form.message-form--editing.message-form--mode-wysiwyg > '
                                      f'div > div.message-form__text-wrap > div.react-measure-wrap > '
                                      f'div.prosemirror-root-dom.ProseMirror").innerHTML={innerHTML}')
                time.sleep(2)


            # 작성하기
            driver.find_element(By.XPATH, '//button[@class="ra-button message-form-submit-control__submit-button ra-button--accent"]').click()
            time.sleep(2)

            # 멘션 리스트에 group이 있을경우 발생하는 알럿 클릭
            if 'group' in agitMention:
                driver.find_element(By.XPATH, '//html/body/div[3]/div/button[1]').click()

        print('□ [Agit Post_schedule] 종료')
    except Exception as e:
        raise Exception('※ [Agit Post_schedule] 오류 : ' + str(e))
    finally:
        # chrome 끄기
        if driver:
            driver.close()


# Agit 새글 작성 ----------------------------------------------------------------
def post_templete(*args):
    """
    [Agit 글양식 작성]

    :Args
       - (필수) agitGroup : 접속하려는 아지트 그룹의 Url
       - (필수) agitTemplete : 글양식 이름
       - (필수) agitBody :  작성하려는 새글의 본문
       - (선택) agitMention : 멘션 대상자
       - (선택) agitAttachment : 첨부파일

    :Example
       - Agit.post_templete(agitGorup, agitTemplete, agitBody, agitMention, agitAttachment)
       - Agit.post_templete([agitGorup, agitTemplete, agitBody, agitMention])
    """
    global driver

    try:
        # 입력받은 인수 할당 ------------------------------------------------------
        if type(args[0]) == list:
            agitGroup = args[0][0]
            agitTemplete = args[0][1]
            agitBody = args[0][2]
            try:
                if not any('C:' in element.upper() for element in args[0][3]):
                    agitMention = args[0][3]
                    agitAttachment = args[0][4]
                else:
                    agitMention = ''
                    agitAttachment = args[0][3]
            except:
                agitMention = args[0][3]
                agitAttachment = ''
        else:
            agitGroup = args[0]
            agitTemplete = args[1]
            agitBody = args[2]
            try:
                if not any('C:' in element.upper() for element in args[3]):
                    agitMention = args[3]
                    agitAttachment = args[4]
                else:
                    agitMention = ''
                    agitAttachment = args[3]
            except:
                agitMention = args[3]
                agitAttachment = ''

        # Agit 로그인 -----------------------------------------------------------
        driver = login(agitGroup)

        # 글양식 탭 이동 ---------------------------------------------------------
        driver.find_element(By.XPATH, '//i[@class="ico ico-wall_form_template"]').click()

        # 템플릿 이동 ------------------------------------------------------------
        # template-message-form__templates div 안에 있는 모든 버튼 찾기
        links = driver.find_elements(By.XPATH, "//div[@class='template-message-form__templates']//a[@class='template-item']")

        # CMS관련 버튼 찾기
        search_link = None
        for link in links:
            if link.text == agitTemplete:
                search_link = link
                break

        # CMS관련 버튼이 존재하는 경우 클릭
        if search_link:
            search_link.click()
        else:
            print("'▷ [Agit Post_templete] 글형식 선택 오류")
            # chrome 끄기
            driver.close()
            time.sleep(2)
            # 새글로 작성
            post_new(agitGroup, agitTemplete, agitBody, agitMention, agitAttachment)
            return None
        # 멘션 대상자 삭제---------------------------------------------------------
        buttons = driver.find_elements(By.XPATH, "//button[@class='multi-value-input__label-delete-button']")
        for button in buttons:
            button.click()
            time.sleep(1)

        # 본문 작성 -------------------------------------------------------------
        print('▷ [Agit Post_templete] 시작')
        strBody = ''
        strSheetInfo = ''

        # 입력받은 본문 나누기 -----------------------------------------------------
        agitBodyList = agitBody.split('\n')

        # 나누어진 문자열마다 tag 붙이기 ---------------------------------------------
        for agitBodyList_idx, agitBodyList_row in enumerate(agitBodyList):
            if '구글시트' in agitBodyList_row:
                sheetName = agitBodyList_row[agitBodyList_row.index(':') + 1:agitBodyList_row.index('|')].strip()
                sheetUrl = agitBodyList_row[agitBodyList_row.index('|') + 1:].strip()
                strSheetInfo = f"<a href={sheetName} target=_blank class=ProseMirror__gdrive rel=noopener referrerpolicy=no-referrer>{sheetUrl}</a>"
                strBody = strBody + '<p>구글시트 : </p>'
                strBody = strBody + '<p>' + strSheetInfo + '</p>'
            elif agitBodyList_row == '':
                strBody = strBody + '<p><br></p>'
            else:
                strBody = strBody + '<p>' + agitBodyList_row + '</p>'

        # 최종적으로 입력 될 본문 할당 -----------------------------------------------
        innerHTML = f'"{strBody}"+' \
                    '"<p><br></p>"+' \
                    '"<p>※ 본 게시글은 RPA가 작성 하였습니다.</p>"'

        # 본문 입력 -------------------------------------------------------------
        print(' ※ 본문 입력')
        pyperclip.copy(agitBody)
        driver.execute_script(f'document.querySelector("#agBody > section > div > '
                              f'div.message-form-group.message-form-group--TEMPLATE > div.message-form-group__body > '
                              f'div > div > div.message-form.message-form--editing.message-form--mode-wysiwyg > div > div.message-form__text-wrap > div.react-measure-wrap > '
                              f'div.prosemirror-root-dom.ProseMirror").innerHTML=""')

        # driver.find_element(By.XPATH, '//*[@id="agBody"]/section/div/div[2]/div[2]/div/div/div[4]/div/div[1]/div[1]/div[1]').click()
        element = driver.find_element(By.XPATH,
                                      '//*[@id="agBody"]/section/div/div[2]/div[2]/div/div/div[4]/div/div[1]/div[1]/div[1]')
        driver.execute_script("arguments[0].click();", element)
        driver.find_element(By.XPATH,
                            '//*[@id="agBody"]/section/div/div[2]/div[2]/div/div/div[4]/div/div[1]/div[1]/div[1]').send_keys(
            Keys.LEFT_CONTROL + 'v')

        time.sleep(2)
        # 멘션 입력 -------------------------------------------------------------
        if agitMention != '':
            print(' ※ 멘션 입력')
            # # 멘션 입력
            # 'End'로 마지막 이동
            driver.find_element(By.XPATH,
                                '//*[@id="agBody"]/section/div/div[2]/div[2]/div/div/div[3]/div[1]/input').send_keys(
                Keys.END)

            # ldap입력 후 대기 2초 후 탭
            for mention in agitMention:
                print('  - ' + mention)
                #driver.find_element(By.XPATH,
                #                    '//*[@id="agBody"]/section/div/div[2]/div[2]/div/div/div[3]/div[1]/input').send_keys(
                #    '@' + mention)
                # XPATH를 사용하여 요소 찾기
                element = driver.find_element(By.XPATH,
                                              '//*[@id="agBody"]/section/div/div[2]/div[2]/div/div/div[3]/div[1]/input')

                # '@'를 먼저 입력
                element.send_keys('@')

                # mention 문자열을 한 글자씩 입력
                for char in mention:
                    element.send_keys(char)
                    time.sleep(0.1)  # 각 문자 입력 사이에 지연을 추가
                time.sleep(2)
                driver.find_element(By.XPATH,
                                    '//*[@id="agBody"]/section/div/div[2]/div[2]/div/div/div[3]/div[1]/input').send_keys(
                    Keys.TAB)

        # 첨부파일 등록 ----------------------------------------------------------
        print(' ※ 첨부파일 등록')
        if agitAttachment != '':
            for agitAttachment_idx, agitAttachment_row in enumerate(agitAttachment):
                # 파일 업로드를 위한 input 요소
                #file_input = driver.find_element(By.XPATH, '//span[@class="message-form__attach-file"]')
                # ActionChains를 사용하여 파일 업로드를 시뮬레이트
                #actions = ActionChains(driver)
                #actions.move_to_element(file_input).click().send_keys(agitAttachment_row.replace(';', ':')).perform()

                # '파일첨부' 클릭
                driver.find_element(By.XPATH, '//span[@class="message-form__attach-file"]').click()
                autoit.win_wait_active("열기", 30)
                time.sleep(2)

                # 첨부파일 경로 입력 후 확인
                autoit.control_send("열기", "Edit1", "^a" + agitAttachment_row.replace(';', ':'))
                time.sleep(2)
                autoit.control_click("열기", "Button1")

                # 업로드 되었는지 확인
                for retry in range(1, 100):
                    try:
                        cancelMark = len(driver.find_elements(By.XPATH,
                                                              '//button[@class="icon-button attachments-box__file-cancel-btn"]'))
                        if cancelMark == retry:
                            print(' - 업로드 완료 : ' + agitAttachment_row)
                            time.sleep(2)
                            break
                        else:
                            time.sleep(1)
                    except:
                        print(' - 첨부파일 업로드 중 : ' + str(retry) + '...')

        # 작성하기
        driver.execute_script(
            'document.querySelector("#agBody > section > div > div.message-form-group.message-form-group--TEMPLATE > '
            'div.message-form-group__body > div > div > div.message-form.message-form--editing.message-form--mode-wysiwyg.message-form--with-files > div > div.message-form__footer > '
            'div.message-form-submit-control > button.ra-button.message-form-submit-control__submit-button.ra-button--accent").click()')
        time.sleep(2)

        # 멘션 리스트에 group이 있을경우 발생하는 알럿 클릭
        if 'group' in agitMention:
            driver.find_element(By.XPATH, '//html/body/div[3]/div/button[1]').click()

        print('□ [Agit Post_templete] 종료')
    except Exception as e:
        raise Exception('※ [Agit Post_templete] 오류 : ' + str(e))
    finally:
        # chrome 끄기
        if driver:
            driver.close()