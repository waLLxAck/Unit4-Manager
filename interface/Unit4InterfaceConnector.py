from PyQt5 import QtWidgets

from model.Project import Project
from util.Initializer import FILE_HANDLER, SETTINGS


def get_all_projects():
    projects = []
    project_files = FILE_HANDLER.get_projects_files()
    for project_file in project_files:
        projects.append(Project.from_json(project_file))
    return projects


# class InformationDisplayWindow:
#     def __init__(self, text_box: QtWidgets.QTextEdit):
#         pass
#
#     def sample_method(self):
#         title = "Sample Title"


class EnvironmentManagementMenu:
    def __init__(self):
        self.PROJECTS = get_all_projects()

    def run_all(self):
        for project in self.PROJECTS:
            project.prepare_environment()
        print("Bookmarks file updated.")
        if SETTINGS.distribute_bookmarks_between_browsers:
            FILE_HANDLER.distribute_bookmarks_from_default_to_other_browsers()

    @staticmethod
    def distribute_bookmarks_across_browsers():
        FILE_HANDLER.distribute_bookmarks_from_default_to_other_browsers()

    def generate_bookmarks(self):
        for project in self.PROJECTS:
            project.generate_bookmarks()
        print("Bookmark generation complete.")

    def build_insomnia_collection(self):
        for project in self.PROJECTS:
            project.build_insomnia_collection()


class Tools:
    def __init__(self, txt_header, txt_row_variable, txt_delimiter):
        self.txt_header = txt_header
        self.txt_row_variable = txt_row_variable
        self.txt_delimiter = txt_delimiter

    def convert_csv_header_to_liquid_variables(self):
        from development_tool.csv_header_into_liquid_variables import convert_header
        convert_header(self.txt_header.toPlainText(), self.txt_row_variable.toPlainText(),
                       self.txt_delimiter.toPlainText())


class ProjectEntryScreen:
    def __init__(self, project_name, swagger_api, urls, environments):
        self.project_name = project_name
        self.swagger_api = swagger_api
        self.urls = urls
        self.environments = environments

    def save_new_project_entry(self):
        project = Project(self.project_name, self.swagger_api, self.urls, self.environments)
        FILE_HANDLER.save_json_file(project.to_json(), project.get_project_name())
        print("Project saved.")
