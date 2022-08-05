import json

from BookmarkManager import BookmarkManager
from InsomniaManager import InsomniaManager


class StandardFileNames:
    def __init__(self):
        self.swagger_base = "SwaggerUI"
        self.extension_kit_base = "Extension Kit"
        self.erp_lab_base = "ERP Lab"

    def get_swagger_name(self, project_short_name, project_full_name):
        return f"{project_short_name} - {project_full_name} - {self.swagger_base} - Unit4"

    def get_extension_kit_name(self, project_short_name, project_full_name, environment):
        return f"{project_short_name} - {project_full_name} - {self.extension_kit_base} - {environment.upper()} - Unit4"

    def get_erp_lab_name(self, project_short_name, project_full_name, environment):
        return f"{project_short_name} - {project_full_name} - {self.erp_lab_base} - {environment.upper()} - Unit4"

    def get_swagger_environment_name(self, project_short_name, project_full_name, environment):
        return f"{project_short_name} - {project_full_name} - {self.swagger_base} - {environment.upper()} - Unit4"

    @staticmethod
    def get_url_name(project_short_name, project_full_name, url_name):
        return f"{project_short_name} - {project_full_name} - {url_name} - Unit4"


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
    def __init__(self, name, extension_kit, erp_lab, authorization, swagger_api, **kwargs):
        self.name = name
        self.extension_kit: str = extension_kit
        self.erp_lab: str = erp_lab
        self.swagger_api: str = swagger_api
        self.authorization = Auth(**authorization)

    @classmethod
    def from_json(cls, json_object):
        return cls(**json_object)


class ProjectUrl:
    def __init__(self, name, url, **kwargs):
        self.name: str = name
        self.url: str = url

    @classmethod
    def from_json(cls, json_object):
        return cls(**json_object)


class Project:
    def __init__(self, project_name, swagger_api: str, urls, environments, **kwargs):
        self.__environments = []
        for environment in environments:
            self.__environments.append(Environment.from_json(environment))
        self.__project_name = project_name
        self.__swagger_api = swagger_api
        self.__urls = []
        for url in urls:
            self.__urls.append(ProjectUrl.from_json(url))
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
                try:
                    return environment.extension_kit.split("/")[-1].split("-")[1].upper()
                except:
                    return environment.extension_kit.split("/")[-1].split("_")[1].upper()
            return environment.erp_lab.split("/")[-1].split("_")[1].upper()
        raise Exception("Project shortname unknown. Extension Kit url splits on '-' and ERP Lab splits on '_'.")

    def __create_project_bookmarks(self, project_folder):
        if self.__swagger_api:
            swagger_name = self.names.get_swagger_name(project_short_name=self.__project_short_name,
                                                       project_full_name=self.__project_name)
            self.bm.create_url(project_folder, swagger_name, self.__swagger_api)
        for environment in self.__environments:
            if environment.extension_kit:
                bookmark_name = self.names.get_extension_kit_name(project_short_name=self.__project_short_name,
                                                                  project_full_name=self.__project_name,
                                                                  environment=environment.name)
                self.bm.create_url(project_folder, bookmark_name, environment.extension_kit)
            if environment.erp_lab:
                bookmark_name = self.names.get_erp_lab_name(project_short_name=self.__project_short_name,
                                                            project_full_name=self.__project_name,
                                                            environment=environment.name)
                self.bm.create_url(project_folder, bookmark_name, environment.erp_lab)
            if environment.swagger_api:
                bookmark_name = self.names.get_swagger_environment_name(project_short_name=self.__project_short_name,
                                                                        project_full_name=self.__project_name,
                                                                        environment=environment.name)
                self.bm.create_url(project_folder, bookmark_name, environment.swagger_api)
        for url in self.__urls:
            if url.name and url.url:
                bookmark_name = self.names.get_url_name(project_short_name=self.__project_short_name,
                                                        project_full_name=self.__project_name,
                                                        url_name=url.name)
                self.bm.create_url(project_folder, bookmark_name, url.url)

    def generate_bookmarks(self):
        self.bm.update_bookmarks()
        unit4_projects_folder = self.bm.get_projects_folder()
        project_folder = self.bm.create_folder(unit4_projects_folder, self.__project_name)
        self.__create_project_bookmarks(project_folder)
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
