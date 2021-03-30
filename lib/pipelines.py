import collections
from dataclasses import dataclass, field
from typing import Sequence, Union, Callable

from lib.filters import Filter, TagFilter, FilterableObject
from lib.mergers import CredentialMerger, CrossCredentialMerger
from lib.models import Login, Password, Credential
from lib.rules import Rule, AppendLastYearsRule


@dataclass
class CredentialPipeline(object):
    mergers: Sequence[CredentialMerger] = field(default_factory=lambda: [CrossCredentialMerger])
    login_filter: Union[Callable[[Login], bool], Filter] = lambda x: True
    password_filter: Union[Callable[[Password], bool], Filter] = lambda x: True
    password_chains: Sequence[Sequence[Rule]] = field(default_factory=lambda: [])

    def build(self, logins: Sequence[Login], passwords: Sequence[Password]):
        filtered_logins = [x for x in logins if self.__match_login_filter(x)]
        filtered_passwords = [x for x in passwords if self.__match_password_filter(x)]
        expanded_passwords = set(filtered_passwords)
        for rule_chain in self.password_chains:
            expanded_passwords.update(self.__apply_password_chain(rule_chain, filtered_passwords))
        credentials = self.__merge_credentials(filtered_logins, expanded_passwords)
        return filtered_logins, expanded_passwords, credentials

    def __apply_password_chain(self, chain: Sequence[Rule], passwords: Sequence[Password]) -> Sequence[Password]:
        pws = passwords
        for rule in chain:
            pws = rule.apply(pws)
        return pws

    def __match_password_filter(self, pw: Password) -> bool:
        return self.password_filter.match(pw) if isinstance(self.password_filter, Filter) else self.password_filter(pw)

    def __match_login_filter(self, login: Login) -> bool:
        return self.login_filter.match(login) if isinstance(self.login_filter, Filter) else self.login_filter(login)

    def __merge_credentials(self, logins: Sequence[Login], passwords: Sequence[Password]) -> Sequence[Credential]:
        creds = set()
        for merger in self.mergers:
            creds.update(merger.combinations(logins, passwords))
        return creds



admin_default = CredentialPipeline(login_filter=(TagFilter('admin') | TagFilter('company')),
                                                       password_filter=TagFilter('admin'))
admin_company = CredentialPipeline(login_filter=TagFilter('admin'),
                                                       password_filter=TagFilter('company'),
                                                       password_chains=[[TagFilter('company'), AppendLastYearsRule(separators=(".", ""))]])
