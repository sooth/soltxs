import abc
from dataclasses import dataclass
from typing import List, Optional

from soltxs import parser


@dataclass(slots=True)
class Resolve:
    pass


class Resolver(abc.ABC):
    @abc.abstractmethod
    def resolve(self, instructions: List[parser.models.ParsedInstruction]) -> Optional[Resolve]:
        raise NotImplementedError
