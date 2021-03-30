import collections
import logging
import sys
from abc import ABC, abstractmethod
from collections import Sequence
from dataclasses import field, dataclass
from typing import TextIO

from lib.filters import FilterableObject
from lib.models import Credential, Password, Login


class Output(ABC):
    @abstractmethod
    def write(self, obs: Sequence[FilterableObject]):
        pass

@dataclass
class ListOutput(Output):
    destination: TextIO = sys.stdout
    source: str = "credentials"

    def write(self, **kwargs):
        obs = kwargs.get(self.source, [])
        logging.debug('\n'.join(["{} - {}".format(str(c), c.reliability) for c in obs]))
        self.destination.write('\n'.join([str(c) for c in obs]))

