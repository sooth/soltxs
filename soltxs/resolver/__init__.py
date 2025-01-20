from typing import List

from soltxs import parser
from soltxs.resolver import models, resolvers


def resolve(parsed: List[parser.models.ParsedInstruction]) -> models.Resolve:
    """
    Translate a list of parsed instructions into a final interpretation.
    """
    for transformer in (resolvers.pumpfun.PumpFunResolver, resolvers.raydium.RaydiumResolver):
        result = transformer.resolve(parsed)
        if result is not None:
            return result

    return resolvers.unknown.UnknownResolver.resolve(parsed)
