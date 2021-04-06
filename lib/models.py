from dataclasses import dataclass, field
from typing import Sequence


@dataclass
class Password(object):
    value: str
    reliability: float = 1.0
    tags: Sequence[str] = field(default_factory=lambda: [])

    def __str__(self):
        return self.value
    def __hash__(self):
        return hash((self.value, self.reliability))

    def __lt__(self, other):
        return self.reliability < other.reliability

    @classmethod
    def from_str(cls, *args, **kwargs):
        return cls(*args, **kwargs)

@dataclass
class Login(object):
    value: str
    reliability: float = 1.0
    tags: Sequence[str] = field(default_factory=lambda: [])

    def __str__(self):
        return self.value

    def __hash__(self):
        return hash((self.value, self.reliability))

    def __lt__(self, other):
        return self.reliability < other.reliability

    @classmethod
    def from_str(cls, *args, **kwargs):
        return cls(*args, **kwargs)

@dataclass
class Credential(object):
    login: Login
    password: Password

    def __str__(self):
        return ':'.join((self.login.value,self.password.value))

    @property
    def reliability(self):
        return self.login.reliability * self.password.reliability

    def __hash__(self):
        return hash((self.login.value, self.password.value, self.reliability))

    def __lt__(self, other):
        return self.reliability < other.reliability

    @classmethod
    def from_str(cls, value:str, *args, **kwargs):
        login_value, password_value = value.split(":", 1)
        return cls(login=Login(login_value, *args, **kwargs), password=Password(password_value, *args, **kwargs))

@dataclass
class Scope(object):
    company: str
    company_abbreviation: str
    keywords: Sequence[str]

