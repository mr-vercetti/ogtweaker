import os
import ctypes
import sys
import requests
import tempfile
import shutil
import json
from ui import UI
from logger import logger
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError
from tqdm import tqdm
from zipfile import ZipFile, BadZipFile


class Tweaker:

    def __init__(self, game, exe_file):
        self.title = 'OGT'
        self.game = game
        self.exe_file = exe_file
        self.ui = UI(self.game)

    def load_config(self):
        if getattr(sys, 'freeze', False):
            # running as bundle (aka frozen)
            bundle_dir = sys._MEIPASS
        else:
            # running live
            bundle_dir = os.path.dirname(os.path.abspath(__file__))

        with open(f'{bundle_dir}//config.json', 'r') as config_file:
            config = json.load(config_file)
        
        return config


    def get_resolution(self):
        """This method checks the resolution of the main screen."""
        user32 = ctypes.windll.user32
        resolution = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return resolution

    def get_drives(self):
        """This method checks what disks are installed in the system."""
        drives = []
        drive_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        try:
            for drive_letter in drive_letters:
                if os.path.exists(f'{drive_letter}:'):
                    drives.append(f'{drive_letter}:\\')
                else:
                    pass
            return drives
        except OSError:
            logger.error('Unable to check your drives, try again as admin.')
            sys.exit(1)

    def get_cwd(self):
        try:
            cwd = os.getcwd()
            return cwd
        except OSError:
            logger.error('Unable to get current dir, try again as admin.')
            sys.exit(1)

    def get_tempdir(self):
        try:
            tempdir = tempfile.gettempdir()
        except OSError:
            logger.error('Unable to get temp dir, try again as admin.')
            sys.exit(1)
        return tempdir

    def get_game_dir_manual(self):
        """This method is needed in case the automatic search does not work."""
        self.ui.print_message('Please provide full path to game installation dir.')
        while True:
            game_dir = self.ui.get_answer()
            exe_path = f'{game_dir}\\{self.exe_file}'
            if not os.path.isfile(exe_path):
                logger.error(f'Unable to find game installation in "{game_dir}"')
            else:
                break
        return game_dir

    def get_game_dir_auto(self):
        """This method is looking for .exe file and returns the path to the
        directory in which it is located. If it cannot find it, it calls the
        get_game_dir_manual method."""
        self.ui.print_message('Searching for the game on your disk...')
        drives = self.get_drives()

        try:
            for drive_root in drives:
                for root, dirs, files in os.walk(drive_root):
                    if self.exe_file in files:
                        exe_path = os.path.join(root, self.exe_file)
                        game_dir = os.path.dirname(exe_path)
#                        There was an list here, but...
#                        The search for all files with specific name takes
#                        an awfully long time, so stop after the first one found.
#                        game_dirs.append(os.path.dirname(exe_path))
                        break
            if game_dir:
                game_dir_correct = self.ui.yes_or_no_menu(f'Is this the correct game path? - {game_dir}')
                if game_dir_correct == 'n':
                    game_dir = self.get_game_dir_manual()
            else:
                logger.error('Unable to find game on your disk')
                game_dir = self.get_game_dir_manual()
        except OSError:
            logger.error('Unable to find game on your disk')
            game_dir = self.get_game_dir_manual()
        return game_dir

    def write_to_file(self, file, data):
        """This method writes data to the file, if it does not exist it creates it,
        if exists it overwrites its content"""
        try:
            with open(file, 'w') as f:
                f.write(data)
        except OSError:
            file = os.path.basename(file)
            logger.error(f'Cannot write to file {file}')
            self.ui.continue_menu()

    def append_to_file(self, file, data):
        """This method appends data to the file."""
        try:
            with open(file, 'a') as f:
                f.write(data)
        except OSError:
            file = os.path.basename(file)
            logger.error(f'Cannot write to file {file}')
            self.ui.continue_menu()

    def copy(self, source, destination):
        try:
            shutil.copy(source, destination)
        except OSError:
            file = os.path.basename(source)
            logger.error(f'Unable to copy file {file}')
            self.ui.continue_menu()

    def remove(self, path):
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        except OSError:
            logger.error(f'Unable to remove {path}')
            self.ui.continue_menu()

    def download(self, url, file):
        """This method downloads a file from the specified URL and
        shows the status bar."""
        try:
            response = requests.get(url, stream=True)
            total = int(response.headers.get('content-length', 0))
            with open(file, 'wb') as f, tqdm(
                desc=file,
                total=total,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
                bar_format="{desc}: {bar}{n_fmt}/{total_fmt} [{rate_fmt}{postfix}]",
            ) as bar:
                for data in response.iter_content(chunk_size=1024):
                    size = f.write(data)
                    bar.update(size)
        except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
            logger.error(f'Unable to download file from {url}')

    def unzip(self, source, destination=None):
        try:
            with ZipFile(source, 'r') as zip_obj:
                zip_obj.extractall(destination)
        except BadZipFile:
            logger.error(f'Unable to unzip - {source}')
            self.ui.continue_menu()

    def download_unzip(self, url, file, destination, remove_zip=True):
        self.download(url, file)
        self.unzip(file, destination)
        if remove_zip:
            self.remove(file)

    def check_path_exists(self, path):
        try:
            exists = os.path.exists(path)
        except OSError:
            logger.error(f'Unable to check if {path} exists')
            self.ui.continue_menu()
        return exists
