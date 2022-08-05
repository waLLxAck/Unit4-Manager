import json
import os
import shutil

import util.Initializer
import util.Paths
from util.Paths import Paths


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

    @staticmethod
    def read_json(path: str):
        return FileHandler.__get_json(FileHandler.__read_file(path))

    def get_settings(self):
        return self.read_json(self.paths.SETTINGS)

    def get_bookmarks_path(self):
        path = util.Paths.get_default_browser_bookmarks_path()
        if not path:
            print("Default browser not found. Defaulting to bookmarks path provided in 'data/settings.json'.")
            path = self.get_settings()["bookmarks_path"]
            if not path:
                raise Exception(
                    "Please provide a path in 'data/settings.json' to your 'Bookmarks' file. Field: bookmarks_path.")
        return path

    def get_bookmarks_chrome(self):
        return self.read_json(self.bookmarks_path)

    @staticmethod
    def save_json_file(file_name, json_object):
        file = open(file_name, "w")
        json.dump(json_object, file, indent=3)

    def save_changes(self, chrome_bookmarks):
        self.save_json_file(self.bookmarks_path, chrome_bookmarks)

    def distribute_bookmarks_from_default_to_other_browsers(self):
        for bookmark_path in self.get_browser_bookmarks_paths():
            shutil.copy2(self.bookmarks_path, bookmark_path)
            print(f"Bookmarks copied from '{self.bookmarks_path}' to '{bookmark_path}'.")

    def get_browser_bookmarks_paths(
            self):  # todo make dynamic -> try to retrieve all Bookmarks in try, except and add to list
        paths = [f"{util.Initializer.app_data_path}\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks"]
        return paths

    @staticmethod
    def get_projects_files():
        paths = Paths()
        project_files = []
        for file in os.listdir(paths.PROJECTS):
            project_files.append(FileHandler.read_json(f"{paths.PROJECTS}/{file}"))
        return project_files

    def has_changes(self, chrome_bookmarks):
        # get the bookmarks file from the default browser
        default_bookmarks = self.get_bookmarks_chrome()
        # check if the bookmarks file has changes
        if default_bookmarks != chrome_bookmarks:
            return True
        else:
            return False
