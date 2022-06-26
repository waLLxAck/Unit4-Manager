class Settings:
    def __init__(self, bookmarks_path, distribute_bookmarks_between_browsers, **kwargs):
        self.bookmarks_path = bookmarks_path
        self.distribute_bookmarks_between_browsers = distribute_bookmarks_between_browsers

    @classmethod
    def from_json(cls, json_object):
        return cls(**json_object)
