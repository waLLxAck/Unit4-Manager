import datetime
import json

import util.Initializer
from util import Helper
from util.Initializer import FILE_HANDLER


class InsomniaCollection:
    def __init__(self, name: str, description="", scope="collection", _type="workspace"):
        self._id = f"wrk_{Helper.generate_random_alphanumeric_string(32)}"
        self.parentId = None
        self.modified = util.Initializer.time_now
        self.created = util.Initializer.time_now
        self.name = name
        self.description = description
        self.scope = scope
        self._type = _type

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, indent=3))

    @property
    def id(self):
        return self._id


class InsomniaGetMethod:
    class Parameter:
        def __init__(self, name, value, description=""):
            self.id = f"pair_{Helper.generate_random_alphanumeric_string(32)}"
            self.name = name
            self.value = value
            self.description = description

        def to_json(self):
            return json.loads(json.dumps(self.__dict__, indent=3))

    def __init__(self, insomnia_collection_id, auths, description="", **kwargs):
        choice = None
        for auth in auths["erp"].keys():
            choice = (auth, auths["erp"][auth])
        if choice is None:
            raise Exception("No authentication selected. Check your environments details.")

        self._id = f"req_{Helper.generate_random_alphanumeric_string(32)}"
        self.parentId = insomnia_collection_id
        self.modified = util.Initializer.time_now
        self.created = util.Initializer.time_now
        self.url = "{{ _.urls.swagger_api }}{% request 'name', '', 0 %}?companyId={{ _.authorization.erp." + choice[
            0] + ".company_id }}"
        self.name = "/v1/objects/attribute-values"
        self.description = description
        self.method = "GET"
        self.body = {}
        self.parameters = [self.Parameter("filter", "attributeId eq 'C1'").to_json()]
        self.headers = []

        self.authentication = {
            "type": "oauth2",
            "grantType": "client_credentials",
            "accessTokenUrl": "{{ _.authorization.erp." + choice[0] + ".access_token_url }}",
            "clientId": "{{ _.authorization.erp." + choice[0] + ".client_id }}",
            "clientSecret": "{{ _.authorization.erp." + choice[0] + ".client_secret }}"
        }
        self.metaSortKey = -1
        self.isPrivate = False
        self.settingStoreCookies = True
        self.settingSendCookies = True
        self.settingDisableRenderRequestBody = False
        self.settingEncodeUrl = True
        self.settingRebuildPath = True
        self.settingFollowRedirects = "global"
        self._type = "request"

    @property
    def id(self):
        return self._id

    @classmethod
    def from_json(cls, json_object):
        return cls(**json_object)

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, indent=3))


class InsomniaBaseEnvironment:
    def __init__(self, insomnia_collection_id, name):
        self._id = f"env_{Helper.generate_random_alphanumeric_string(32)}"
        self.parentId = insomnia_collection_id
        self.modified = util.Initializer.time_now
        self.created = util.Initializer.time_now
        self.name = name
        self.data = {}
        self.dataPropertyOrder = {}
        self.color = None
        self.isPrivate = False
        self.metaSortKey = util.Initializer.time_now
        self._type = "environment"

    @property
    def id(self):
        return self._id

    @classmethod
    def from_json(cls, json_object):
        return cls(**json_object)

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, indent=3))


class SubEnvironment:
    def __init__(self, insomnia_base_environment_id, name, swagger_api_url_trimmed, auths):
        self._id = f"env_{Helper.generate_random_alphanumeric_string(32)}"
        self.parentId = insomnia_base_environment_id
        self.modified = util.Initializer.time_now
        self.created = util.Initializer.time_now
        self.name = name
        self.data = {
            "urls": {
                "swagger_api": swagger_api_url_trimmed
            },
            "authorization": auths
        }
        self.dataPropertyOrder = {
             "&": [
                 "urls",
                 "authorization"
             ],
             "&~|urls": [
                 "swagger_api"
             ],
             "&~|authorization": [
                 "erp"
             ],
             "&~|authorization~|erp": [
                 "prev",
                 "acpt",
                 "prod"
             ],
             "&~|authorization~|erp~|prev": [
                 "company_id",
                 "access_token_url",
                 "client_id",
                 "client_secret"
             ],
             "&~|authorization~|erp~|acpt": [
                 "company_id",
                 "access_token_url",
                 "client_id",
                 "client_secret"
             ],
             "&~|authorization~|erp~|prod": [
                 "company_id",
                 "access_token_url",
                 "client_id",
                 "client_secret"
             ]
         }
        self.color = None
        self.isPrivate = False
        self.metaSortKey = util.Initializer.time_now
        self._type = "environment"

    @classmethod
    def from_json(cls, json_object):
        return cls(**json_object)

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, indent=3))


class DefaultCookieJar:
    def __init__(self, insomnia_base_environment_id, name="Default Jar"):
        self._id = f"jar_{Helper.generate_random_alphanumeric_string(32)}"
        self.parentId = insomnia_base_environment_id
        self.modified = util.Initializer.time_now
        self.created = util.Initializer.time_now
        self.name = name
        self.cookies = []
        self._type = "cookie_jar"

    @classmethod
    def from_json(cls, json_object):
        return cls(**json_object)

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, indent=3))


class APISpec:
    def __init__(self, insomnia_base_environment_id, project_name):
        self._id = f"spc_{Helper.generate_random_alphanumeric_string(32)}"
        self.parentId = insomnia_base_environment_id
        self.modified = util.Initializer.time_now
        self.created = util.Initializer.time_now
        self.fileName = project_name
        self.contents = ""
        self.contentType = "yaml"
        self._type = "api_spec"

    @classmethod
    def from_json(cls, json_object):
        return cls(**json_object)

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, indent=3))


class InsomniaManager:
    def __init__(self, project_name, auths, swagger_url_trimmed, _type="export", __export_format=4,
                 __export_source="insomnia.desktop.app:v2022.4.2"):
        self._type = _type
        self.__export_format = __export_format
        self.__export_date = str(datetime.datetime.today())
        self.__export_source = __export_source
        insomnia_collection = InsomniaCollection(project_name)
        insomnia_base_environment = InsomniaBaseEnvironment(insomnia_collection.id, "Base Environment")
        self.resources = [
            InsomniaGetMethod(insomnia_collection.id, auths).to_json(),
            insomnia_collection.to_json(),
            insomnia_base_environment.to_json(),
            DefaultCookieJar(insomnia_collection.id).to_json(),
            APISpec(insomnia_collection.id, project_name).to_json(),
            SubEnvironment(insomnia_base_environment.id, project_name, swagger_url_trimmed, auths).to_json()
        ]

    @classmethod
    def from_json(cls, json_object):
        return cls(**json_object)

    def to_json(self):
        return {
            "_type": self._type,
            "__export_format": self.__export_format,
            "__export_date": self.__export_date,
            "__export_source": self.__export_source,
            "resources": self.resources
        }

    def generate_insomnia_file(self, project_name):
        file_name = f"Insomnia_{project_name}_{datetime.date.today()}.json"
        FILE_HANDLER.save_json_file(file_name, self.to_json())
        print(f"{file_name} was created in '/' directory.")
