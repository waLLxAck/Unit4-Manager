from util.FileHandler import FileHandler
from Project import Project

for project_json in FileHandler().get_new_imports():
    project = Project.from_json(project_json)
    # project.generate_bookmarks()
    project.build_insomnia_collection()

