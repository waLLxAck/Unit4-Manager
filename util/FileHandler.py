import json
import os
import shutil

import util.Initializer
from util import Helper


class Paths:
    INSOMNIA_COLLECTIONS = "insomnia_collections"
    SETTINGS = "settings.json"
    PROJECTS = "data/projects"


class FileHandler:
    def __init__(self):
        self.paths = Paths()
        self.bookmarks_path = self.get_bookmarks_path()

    @staticmethod
    def __get_json(file):
        return json.loads(file)

    @staticmethod
    def __read_file(file_path: str):
        with open(file_path, encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def read_json(path: str):
        return FileHandler.__get_json(FileHandler.__read_file(path))

    def get_settings(self):
        return self.read_json(self.paths.SETTINGS)

    def get_bookmarks_path(self):
        path = Helper.get_default_browser_bookmarks_path()
        if not path:
            print("Default browser not found. Defaulting to bookmarks path provided in 'data/settings.json'.")
            path = self.get_settings()["bookmarks_path"]
            if not path:
                raise Exception("Missing field: bookmarks_path. Please provide a path in 'settings.json' to your 'Bookmarks' file.")
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

    def get_browser_bookmarks_paths(self):
        # todo retrieve all bookmark files??
        paths = [f"{util.Initializer.app_data_path}\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks"]
        return paths

    @staticmethod
    def get_projects_files():
        project_files = []
        for file in os.listdir(Paths.PROJECTS):
            project_files.append(FileHandler.read_json(f"{Paths.PROJECTS}/{file}"))
        return project_files

    @staticmethod
    def create_folders_if_not_exists():
        for folder in [Paths.INSOMNIA_COLLECTIONS, Paths.PROJECTS]:
            if not os.path.exists(folder):
                os.makedirs(folder)
                print(f"Folder '{folder}' created.")

    @staticmethod
    def create_settings_file_if_not_exists():
        if not os.path.exists(Paths.SETTINGS):
            FileHandler.save_json_file(Paths.SETTINGS, {
                "bookmarks_path": "",
                "distribute_bookmarks_between_browsers": True,
                "projects_path": "Unit4/Projects"
            })
            print("Settings file created.")
