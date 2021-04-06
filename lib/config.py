import sys

import yaml

from lib.context import Context
from lib.models import Scope, Login, Password, Credential
from lib.outputs import ListOutput
import lib.pipeline
import lib.generators


class ListOutputBuilder(yaml.YAMLObject):
    yaml_tag = "!ListOutput"

    @classmethod
    def from_yaml(cls, loader, node):
        d = loader.construct_mapping(node)
        dst = d.get("destination", None)
        d['destination'] = sys.stdout if dst is None or dst == '-' else open(dst, "w")
        output = ListOutput(**d)
        return output


class ScopeBuilder(yaml.YAMLObject):
    yaml_tag = "!Scope"

    @classmethod
    def from_yaml(cls, loader, node):
        scope_dict = loader.construct_mapping(node, deep=True)
        scope = Scope(**scope_dict)
        return scope


class FileInput(yaml.YAMLObject):
    yaml_tag = "!FileInput"

    def __init__(self, path, **kwargs):
        self.path = path
        self.args = kwargs

    def objects(self, cls):
        with open(self.path) as f:
            for value in f.read().strip().split("\n"):
                vs = value.strip()
                if len(vs) > 0:
                    yield cls.from_str(vs, **self.args)

    @classmethod
    def from_yaml(cls, loader, node):
        d = loader.construct_mapping(node)
        return cls(**d)


class ListInput(yaml.YAMLObject):
    yaml_tag = "!ListInput"

    def __init__(self, values, **kwargs):
        self.values = values
        self.args = kwargs

    def objects(self, cls):
        for value in self.values:
            yield cls.from_str(value, **self.args)

    @classmethod
    def from_yaml(cls, loader, node):
        d = loader.construct_mapping(node)
        return cls(**d)


class ContextBuilder(yaml.YAMLObject):
    yaml_tag = "!Context"
    inputs = {}
    pipelines = []
    generators = []

    def context(self, scope):
        logins = self.__logins()
        passwords = self.__passwords()
        credentials = self.__credentials()
        pipelines = self.__pipelines()
        return Context(name=self.name, scope=scope, logins=self.__logins(), passwords=self.__passwords(),
                       credentials=self.__credentials(), pipelines=self.__pipelines(), generators=self.__generators(), outputs=self.outputs)

    def __logins(self):
        login_inputs = self.inputs.get('logins', [])
        logins = set()
        for inp in login_inputs:
            ls = inp.objects(Login)
            logins.update(ls)
        return logins

    def __passwords(self):
        password_inputs = self.inputs.get('passwords', [])
        passwords = set()
        for inp in password_inputs:
            ls = inp.objects(Password)
            passwords.update(ls)
        return passwords

    def __credentials(self):
        credential_inputs = self.inputs.get('credentials', [])
        credentials = set()
        for inp in credential_inputs:
            ls = inp.objects(Credential)
            credentials.update(ls)
        return credentials

    def __pipelines(self):
        pipelines = []
        for pipe_name in self.pipelines:
            try:
                pipelines.append(getattr(lib.pipeline, pipe_name))
            except AttributeError:
                raise "Could not find pipeline {}".format(pipe_name)
        return pipelines

    def __generators(self):
        generators = []
        for generator_name in self.generators:
            try:
                generators.append(getattr(lib.generators, generator_name))
            except AttributeError:
                raise "Could not find generator {}".format(generator_name)
        return generators

class KeuleConfig(object):
    def __init__(self, config_file):
        yaml.add_path_resolver('!Scope', ['scope'], dict)
        yaml.add_path_resolver('!Context', ['contexts', None], dict)
        self.data = yaml.load(config_file, Loader=yaml.Loader)
        self.scope = self.data["scope"]
        self.contexts = []
        for ct_bldr in self.data.get('contexts', []):
            self.contexts.append(ct_bldr.context(scope=self.scope))
