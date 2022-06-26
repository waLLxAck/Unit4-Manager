import uuid
from time import time

from util.FileHandler import FileHandler


class BookmarkManager:
    class BookmarkType:
        FOLDER = "folder"
        URL = "url"

    def __init__(self):
        self.file_handler = FileHandler()
        self.chrome_bookmarks = self.file_handler.get_bookmarks_chrome()

    def __get_root_level_bookmarks(self):
        return self.chrome_bookmarks["roots"]["bookmark_bar"]

    def __search_bookmark(self, start_location, bookmark_name, bookmark_type=BookmarkType.URL):
        for bookmark in self.__get_children(start_location):
            if bookmark["name"] == bookmark_name and bookmark["type"] == bookmark_type:
                return bookmark

    @staticmethod
    def __get_children(bookmark) -> list:
        return bookmark["children"]

    def get_unit4_folder(self):
        return self.__search_bookmark(self.__get_root_level_bookmarks(), "Unit4",
                                      self.BookmarkType.FOLDER)

    def get_projects_folder(self):
        return self.__search_bookmark(self.get_unit4_folder(), "Projects",
                                      self.BookmarkType.FOLDER)

    def create_folder(self, bookmark_folder_root, folder_name):
        if self.__search_bookmark(bookmark_folder_root, folder_name, self.BookmarkType.FOLDER):
            return self.__search_bookmark(bookmark_folder_root, folder_name,
                                          self.BookmarkType.FOLDER)
        time_string = str(time())
        folder = {
            "children": [
            ],
            "date_added": time_string,
            "date_modified": time_string,
            "guid": str(uuid.uuid4()),
            "id": "1636",
            "name": folder_name,
            "type": "folder"
        }
        self.__get_children(bookmark_folder_root).append(folder)
        print(f"Folder '{folder_name}' created.")
        return self.__search_bookmark(bookmark_folder_root, folder_name, self.BookmarkType.FOLDER)

    def create_url(self, bookmark_folder_root, bookmark_name: str, url: str):
        if self.__search_bookmark(bookmark_folder_root, bookmark_name):
            return
        time_string = str(time())
        url_bookmark = {
            "date_added": time_string,
            "guid": str(uuid.uuid4()),
            "id": "1635",
            "meta_info": {
                "imageData": "https://sync-thumbnails.operacdn.com/c75a52acc5452f58075c8f31b3077227b3546dddda6f578c6e12b511ee850c68.jpe",
                "imageDataType": "2",
                "imageID": "1795D60FF3E10A3C72E93565696A3F16067CF88426D95776A402B65D36015AFD",
                "imageIdentifier": "23c9aa7c",
                "imageType": "2"
            },
            "name": bookmark_name,
            "type": "url",
            "url": url
        }
        self.__get_children(bookmark_folder_root).append(url_bookmark)
        print(f"URL '{bookmark_name}' created.")

    def commit_changes(self):
        self.file_handler.save_changes(self.chrome_bookmarks)
        print("Bookmarks file updated.")
