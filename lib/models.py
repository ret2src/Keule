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


@dataclass
class Scope(object):
    company: str
    keywords: Sequence[str]


