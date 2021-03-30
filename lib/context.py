from dataclasses import dataclass, field
from typing import Sequence

from lib.models import Scope, Login, Password, Credential
from lib.outputs import Output
from lib.pipelines import CredentialPipeline
from lib.rules import LimitRule, Rule


@dataclass
class Context(object):
    pipelines: Sequence[CredentialPipeline]
    scope: Scope
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
        # todo generate combinations from scope
        self.logins.append(Login(self.scope.company.lower(), tags=('company')))
        self.passwords.append(Password(self.scope.company.lower(), tags=('company')))