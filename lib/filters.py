from dataclasses import dataclass
from typing import Sequence, TypeVar

from lib.models import Login, Password

FilterableObject = TypeVar('FilterableObject', Login, Password)
class Filter(object):
    def match(self, o: FilterableObject) -> bool:
        return True

    def __invert__(self):
        return lambda x: not self.match(x)

    def __or__(self, other):
        return lambda x: self.match(x) or other.match(x)

    def __and__(self, other):
        return lambda x: self.match(x) and other.match(x)

    def apply(self, os: Sequence[FilterableObject]) -> Sequence[FilterableObject]:
        return [x for x in os if self.match(x)]

@dataclass
class TagFilter(Filter):
    tag: str

    def match(self, o: FilterableObject) -> bool:
        return self.tag in o.tags