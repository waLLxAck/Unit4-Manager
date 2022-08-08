from model.Project import Project
from model.Settings import Settings
from util.Initializer import FILE_HANDLER


def run():
    FILE_HANDLER.create_folders_if_not_exists()
    FILE_HANDLER.create_settings_file_if_not_exists()
    settings = Settings.from_json(FILE_HANDLER.get_settings())
    project_files = FILE_HANDLER.get_projects_files()
    for project_file in project_files:
        project = Project.from_json(project_file)
        project.prepare_environment()
    print("Bookmarks file updated.")
    if settings.distribute_bookmarks_between_browsers:
        FILE_HANDLER.distribute_bookmarks_from_default_to_other_browsers()
