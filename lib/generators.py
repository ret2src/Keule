from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Sequence

from lib.models import Scope, Password, Login, Credential

@dataclass
class ScopedGenerator(ABC):

    @property
    @abstractmethod
    def credentials(self) -> Sequence[Credential]:
        return []

    @property
    @abstractmethod
    def logins(self) -> Sequence[Login]:
        return []

    @property
    @abstractmethod
    def passwords(self) -> Sequence[Password]:
        return []


@dataclass
class ScopedCompanyGenerator(ScopedGenerator):
    scope: Scope
    reliability: int = 1.0

    @property
    def __company_name(self):
        return self.scope.company.lower().split(" ")[0]

    @property
    def __company_short(self):
        return self.scope.company_abbreviation.lower()

    @property
    def credentials(self) -> Sequence[Credential]:
        return []

    @property
    def logins(self) -> Sequence[Login]:
        return [Login(self.__company_name, reliability=self.reliability, tags=('company')),
                Login(self.__company_short, reliability=self.reliability, tags=('company', 'company_abbreviation'))]

    @property
    def passwords(self) -> Sequence[Password]:
        return [Password(self.__company_name, reliability=self.reliability, tags=('company')),
                Password(self.__company_short, reliability=self.reliability, tags=('company', 'company_abbreviation'))]

scoped_company = ScopedCompanyGenerator