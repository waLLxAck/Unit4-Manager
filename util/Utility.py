import os
import platform
import random
import string
from time import time

time_now = int(time())


def generate_random_alphanumeric_string(number_of_characters):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=number_of_characters))


def get_default_browser_bookmarks_path():
    osPlatform = platform.system()
    app_data_path = "\\".join(os.getenv('APPDATA').split("\\")[:-1])

    if osPlatform == 'Windows':
        # Find the default browser by interrogating the registry
        from winreg import HKEY_CLASSES_ROOT, HKEY_CURRENT_USER, OpenKey, QueryValueEx

        with OpenKey(HKEY_CURRENT_USER,
                     r'SOFTWARE\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice') as regkey:
            # Get the user choice
            browser_choice = QueryValueEx(regkey, 'ProgId')[0]

        with OpenKey(HKEY_CLASSES_ROOT, r'{}\shell\open\command'.format(browser_choice)) as regkey:
            # Get the application the user's choice refers to in the application registrations
            browser_path_tuple = QueryValueEx(regkey, None)

            # This is a bit sketchy and assumes that the path will always be in double quotes
            browser_path = browser_path_tuple[0].split('"')[1]

            bookmarks_path = app_data_path

            if "Chrome" in browser_path:
                bookmarks_path += "\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks"
            elif "Opera" in browser_path:
                bookmarks_path += "\\Roaming\\Opera Software\\Opera Stable\\Bookmarks"
            elif "Internet Explorer" in browser_path:
                raise Exception(
                    "Internet Explorer not supported. Consider upgrading your browser. (Supported Browsers: Opera, Chrome, Edge)")
            elif "Edge" in browser_path:
                bookmarks_path += "\\Local\\Microsoft\\Edge\\User Data\\Default\\Bookmarks"

            if bookmarks_path != app_data_path:
                return bookmarks_path
