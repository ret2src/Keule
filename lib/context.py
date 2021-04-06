from dataclasses import dataclass, field
from typing import Sequence

from lib.generators import ScopedGenerator
from lib.models import Scope, Login, Password, Credential
from lib.outputs import Output
from lib.pipeline.credential_pipeline import CredentialPipeline
from lib.rules import LimitRule, Rule


@dataclass
class Context(object):
    name: str
    pipelines: Sequence[CredentialPipeline]
    scope: Scope
    generators: [ScopedGenerator] = field(default_factory=lambda: [])
    logins: [Login] = field(default_factory=lambda: [])
    passwords: [Password] = field(default_factory=lambda: [])
    credentials: [Credential] = field(default_factory=lambda: [])
    outputs: [Output] = field(default_factory=lambda: [])
    password_output_rule: Rule = field(default_factory=lambda: LimitRule(count=100))
    login_output_rule: Rule = field(default_factory=lambda: LimitRule(count=100))
    credential_output_rule: Rule = field(default_factory=lambda: LimitRule(count=100))
    login_limit: int = 100
    credential_limit: int = 100

    def build(self):
        self.__add_from_scope()
        creds = set(self.credentials)
        logins = set()
        passwords = set()

        for pipeline in self.pipelines:
            ls, ps, cs = pipeline.build(self.logins, self.passwords)
            logins.update(ls)
            passwords.update(ps)
            creds.update(cs)
        creds = self.credential_output_rule.apply(creds)
        logins = self.login_output_rule.apply(logins)
        passwords = self.password_output_rule.apply(passwords)

        for output in self.outputs:
            output.write(logins=logins, passwords=passwords, credentials=creds)

    def __add_from_scope(self):
        for generator_cls in self.generators:
            generator = generator_cls(self.scope)
            self.logins.update(generator.logins)
            self.passwords.update(generator.passwords)
            self.credentials.update(generator.credentials)

