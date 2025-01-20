from soltxs.normalizer import normalize
from soltxs.parser import parse
from soltxs.resolver import resolve

from soltxs import normalizer, parser, resolver


def process(tx: dict) -> resolver.models.Resolve:
    """
    Resolves a Solana transaction.
    """
    normalized = normalize(tx)
    parsed = parse(normalized)
    resolved = resolve(parsed)

    return resolved
