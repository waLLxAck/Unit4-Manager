import os
import platform
from time import time

from model.Settings import Settings
from util.FileHandler import FileHandler

FILE_HANDLER = FileHandler()
SETTINGS = Settings.from_json(FILE_HANDLER.get_settings())

time_now = int(time())
if platform.system() == "Windows":
    app_data_path = "\\".join(os.getenv('APPDATA').split("\\")[:-1])
