import json


class Paths:
    SETTINGS = "settings.json"
    NEW_IMPORTS = "new_bookmarks.json"


class FileHandler:
    def __init__(self):
        self.paths = Paths()
        self.bookmarks_path = self.get_bookmarks_path()

    @staticmethod
    def __get_json(file):
        return json.loads(file)

    @staticmethod
    def __read_file(file_path: str):
        return open(file_path).read()

    def __read_json(self, path: str):
        return self.__get_json(self.__read_file(path))

    def get_settings(self):
        return self.__read_json(self.paths.SETTINGS)

    def get_new_imports(self):
        return self.__read_json(self.paths.NEW_IMPORTS)

    def get_bookmarks_path(self):
        return self.get_settings()["bookmarks_path"]

    def get_bookmarks_chrome(self):
        return self.__read_json(self.get_settings()["bookmarks_path"])

    def save_json_file(self, file_name, json_object):
        file = open(file_name, "w")
        json.dump(json_object, file, indent=3)

    def save_changes(self, chrome_bookmarks):
        self.save_json_file(self.bookmarks_path, chrome_bookmarks)
