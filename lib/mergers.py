from typing import Sequence

from lib.models import Login, Password, Credential


class CredentialMerger(object):
    @classmethod
    def combinations(cls, logins: Sequence[Login], passwords: Sequence[Password]) -> Sequence[Credential]:
        return []


class CrossCredentialMerger(CredentialMerger):
    @classmethod
    def combinations(cls, logins: Sequence[Login], passwords: Sequence[Password]) -> Sequence[Credential]:
        for login in logins:
            for password in passwords:
                yield Credential(login=login, password=password)