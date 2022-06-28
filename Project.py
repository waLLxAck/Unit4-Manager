import json

from BookmarkManager import BookmarkManager
from InsomniaManager import InsomniaManager


class StandardFileNames:
    def __init__(self):
        self.swagger_base = "SwaggerUI"
        self.extension_kit_base = "Extension Kit"
        self.erp_lab_base = "ERP Lab"
        pass

    def get_swagger_name(self, project_short_name, project_full_name):
        return f"{project_short_name} - {project_full_name} - {self.swagger_base} - Unit4"

    def get_extension_kit_name(self, project_short_name, project_full_name, environment):
        return f"{project_short_name} - {project_full_name} - {self.extension_kit_base} - {environment} - Unit4"

    def get_erp_lab_name(self, project_short_name, project_full_name, environment):
        return f"{project_short_name} - {project_full_name} - {self.erp_lab_base} - {environment} - Unit4"


class Auth:
    def __init__(self, company_id, access_token_url, client_id, client_secret, **kwargs):
        self.company_id = company_id
        self.access_token_url = access_token_url
        self.client_id = client_id
        self.client_secret = client_secret

    @classmethod
    def from_json(cls, json_object):
        return cls(**json_object)

    def to_json(self):
        return json.loads(json.dumps(self.__dict__))


class Environment:
    def __init__(self, name, extension_kit, erp_lab, authorization, **kwargs):
        self.name = name
        self.extension_kit: str = extension_kit
        self.erp_lab: str = erp_lab
        self.authorization = Auth(**authorization)

    @classmethod
    def from_json(cls, json_object):
        return cls(**json_object)

    def get_name(self):
        if not self.erp_lab:
            if not self.extension_kit:
                raise Exception("Cannot retrieve Environment name.")
            return self.extension_kit.split("/")[-1].split("-")[-1].upper()
        return self.erp_lab.split("/")[-1].split("_")[-1].upper()


class Project:
    def __init__(self, project_name, swagger_api: str, environments, **kwargs):
        self.__environments = []
        for environment in environments:
            self.__environments.append(Environment.from_json(environment))
        self.__project_name = project_name
        self.__swagger_api = swagger_api
        self.bm = BookmarkManager()
        self.names = StandardFileNames()
        self.__project_short_name = self.get_project_short_name()
        self.im = self.build_insomnia_manager()

    @classmethod
    def from_json(cls, json_object):
        return cls(**json_object)

    def get_project_short_name(self):
        for environment in self.__environments:
            if not environment.erp_lab:
                if not environment.extension_kit:
                    continue
                return environment.extension_kit.split("/")[-1].split("-")[1].upper()
            return environment.erp_lab.split("/")[-1].split("_")[1].upper()
        raise Exception("Project shortname unknown. Extension Kit url splits on '-' and ERP Lab splits on '_'.")

    def __create_swagger_bookmark(self, project_folder):
        swagger_name = self.names.get_swagger_name(project_short_name=self.__project_short_name,
                                                   project_full_name=self.__project_name)
        self.bm.create_url(project_folder, swagger_name, self.__swagger_api)

    def __create_environment_bookmarks(self, project_folder):
        for environment in self.__environments:
            if environment.extension_kit:
                environment_name = environment.get_name()
                bookmark_name = self.names.get_extension_kit_name(project_short_name=self.__project_short_name,
                                                                  project_full_name=self.__project_name,
                                                                  environment=environment_name)
                self.bm.create_url(project_folder, bookmark_name, environment.extension_kit)
            if environment.erp_lab:
                environment_name = environment.get_name()
                bookmark_name = self.names.get_erp_lab_name(project_short_name=self.__project_short_name,
                                                            project_full_name=self.__project_name,
                                                            environment=environment_name)
                self.bm.create_url(project_folder, bookmark_name, environment.erp_lab)

    def generate_bookmarks(self):
        unit4_projects_folder = self.bm.get_projects_folder()
        project_folder = self.bm.create_folder(unit4_projects_folder, self.__project_name)
        self.__create_swagger_bookmark(project_folder)
        self.__create_environment_bookmarks(project_folder)
        self.bm.commit_changes()

    def build_insomnia_collection(self, project_name):
        self.im.generate_insomnia_file(project_name)

    def build_insomnia_manager(self):
        swagger_url_trimmed = self.__swagger_api.split("/swagger")[0]
        auths = {"erp": {}}
        for environment in self.__environments:
            auths["erp"][environment.name] = environment.authorization.to_json()
        return InsomniaManager(self.__project_name, auths, swagger_url_trimmed)

    def prepare_environment(self, generate_bookmarks=True, build_insomnia_collection=True):
        if generate_bookmarks:
            self.generate_bookmarks()
        if build_insomnia_collection:
            self.build_insomnia_collection(self.__project_name)
