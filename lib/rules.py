import collections
from dataclasses import dataclass, field
from datetime import datetime
from typing import Sequence

from lib.filters import FilterableObject
from lib.models import Password


class Rule(object):
    def apply(self, pws: Sequence[FilterableObject]) -> Sequence[FilterableObject]:
        return []


@dataclass
class AppendLastYearsRule(Rule):
    count: int = 10
    separators: Sequence[str] = field(default_factory=lambda: [''])
    current_year = datetime.now().year

    def apply(self, pws: Sequence[Password]) -> Sequence[Password]:
        for pw in pws:
            yield pw
            for x in range(self.count):
                for sep in self.separators:
                    yield Password(value=pw.value + sep + str(self.current_year - x),
                                   reliability=pw.reliability - (0.03 * x), tags=('year', *pw.tags))


@dataclass
class LimitRule(Rule):
    count: int = 50

    def apply(self, objs: Sequence[FilterableObject]) -> Sequence[FilterableObject]:
        res = collections.OrderedDict()
        for obj in sorted(objs, reverse=True):
            if str(obj) not in res:
                res[str(obj)] = obj
        return res.values()
