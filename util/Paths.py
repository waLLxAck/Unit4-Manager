import os
import platform
from pathlib import Path


class Paths:
    def __init__(self):
        self.ROOT = self.get_project_root()
        self.SETTINGS = self.get_settings()
        self.NEW_IMPORTS = self.get_new_imports()
        self.PROJECTS = self.get_projects()
        self.INSOMNIA_COLLECTIONS = self.get_insomnia_collections()

    @staticmethod
    def get_project_root():
        return str(Path(__file__).parent.parent)

    def get_settings(self):
        return self.ROOT + "/data/settings.json"

    def get_new_imports(self):
        return self.ROOT + "/data/new_bookmarks.json"

    def get_projects(self):
        return self.ROOT + "/data/projects"

    def get_insomnia_collections(self):
        return self.ROOT + "/data/insomnia_collections"


def get_default_browser_bookmarks_path():
    osPlatform = platform.system()
    if osPlatform == 'Windows':
        app_data_path = "\\".join(os.getenv('APPDATA').split("\\")[:-1])
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
    elif osPlatform == 'Linux':
        base_path = "/home/" + os.getenv("USER") + "/.config/"
        bookmarks_path = base_path
        default_browser = os.popen("xdg-mime query default x-scheme-handler/http").read().strip()
        if default_browser == 'brave-browser.desktop':
            bookmarks_path += 'BraveSoftware/Brave-Browser/Default/Bookmarks'
        if bookmarks_path != base_path:
            return bookmarks_path
