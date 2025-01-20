from dataclasses import dataclass
from typing import List, Optional

from soltxs import parser
from soltxs.resolver.models import Resolver, Resolve


@dataclass(slots=True)
class Unknown(Resolve):
    pass


class _UnknownResolver(Resolver):
    def resolve(self, instructions: List[parser.models.ParsedInstruction]) -> Resolve:
        return Unknown()


UnknownResolver = _UnknownResolver()
