from Project import Project
from model.Settings import Settings
from util.FileHandler import FileHandler


def run():
    fh = FileHandler()
    settings = Settings.from_json(fh.get_settings())
    for project_json in fh.get_new_imports():
        project = Project.from_json(project_json)
        project.prepare_environment()
        if settings.distribute_bookmarks_between_browsers:
            FileHandler().distribute_bookmarks_from_default_to_other_browsers()


if __name__ == '__main__':
    run()
