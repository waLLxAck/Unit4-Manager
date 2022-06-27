import os
from time import time

from util.FileHandler import FileHandler

FILE_HANDLER = FileHandler()
time_now = int(time())
app_data_path = "\\".join(os.getenv('APPDATA').split("\\")[:-1])
