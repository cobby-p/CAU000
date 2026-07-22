import os
import shutil
import datetime
import logging

class FileUtility:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        #file_handler = logging.FileHandler('file_utility.log')
        #file_handler.setFormatter(formatter)
        #self.logger.addHandler(file_handler)

    def delete_old_files(self, days=30):
        try:
            # 현재 날짜와 지정된 일 수 이전의 날짜 계산
            current_date = datetime.datetime.now()
            threshold_date = current_date - datetime.timedelta(days=days)

            # 폴더 내 파일들을 반복하면서 날짜를 확인하고 삭제
            for file_name in os.listdir(self.folder_path):
                file_path = os.path.join(self.folder_path, file_name)
                # 파일인지 확인하고, 파일의 수정 시간을 가져옴
                if os.path.isfile(file_path):
                    modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                    # 파일의 수정 시간이 지정된 기간 이전이면 삭제
                    if modified_time < threshold_date:
                        os.remove(file_path)
                        self.logger.info(f"Deleted file: {file_path}")
        except Exception as e:
            self.logger.error(f"An error occurred while deleting files: {e}")

    def move_files_by_extension(self, target_folder, extensions):
        try:
            # 대상 폴더가 없는 경우 생성
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            # 지정된 확장자를 가진 파일을 대상 폴더로 이동
            for file_name in os.listdir(self.folder_path):
                file_path = os.path.join(self.folder_path, file_name)
                # 파일인지 확인하고, 지정된 확장자를 가진 경우 대상 폴더로 이동
                if os.path.isfile(file_path):
                    file_extension = os.path.splitext(file_name)[1].lower()
                    if file_extension in extensions:
                        shutil.move(file_path, os.path.join(target_folder, file_name))
                        self.logger.info(f"Moved file: {file_name} to {target_folder}")
        except Exception as e:
            self.logger.error(f"An error occurred while moving files: {e}")

    def create_backup(self, backup_folder):
        try:
            # 백업 폴더가 없는 경우 생성
            if not os.path.exists(backup_folder):
                os.makedirs(backup_folder)

            # 현재 날짜를 기반으로 백업 파일명 생성
            current_date = datetime.datetime.now().strftime('%Y-%m-%d')
            backup_file_name = f"backup_{current_date}.zip"
            backup_file_path = os.path.join(backup_folder, backup_file_name)

            # 폴더를 zip 파일로 압축하여 백업
            shutil.make_archive(backup_file_path[:-4], 'zip', self.folder_path)
            self.logger.info(f"Created backup: {backup_file_path}")
        except Exception as e:
            self.logger.error(f"An error occurred while creating backup: {e}")