from dataclasses import dataclass
from typing import List, Optional

from soltxs import parser
from soltxs.resolver.models import Resolve, Resolver

WSOL_MINT = "So11111111111111111111111111111111111111112"
SOL_MINT = "11111111111111111111111111111111"


@dataclass(slots=True)
class Raydium(Resolve):
    type: str
    who: str
    from_token: str
    from_amount: int
    to_token: str
    to_amount: int
    minimum_amount_out: int


class _RaydiumResolver(Resolver):
    def resolve(self, instructions: List[parser.models.ParsedInstruction]) -> Optional[Resolve]:
        instrs = [i for i in instructions if isinstance(i, parser.parsers.raydiumAMM.Swap)]
        if len(instrs) == 1:
            instr = instrs[0]

            raydium_type = "swap"
            if instr.from_token in {WSOL_MINT, SOL_MINT}:
                raydium_type = "buy"
            elif instr.to_token in {WSOL_MINT, SOL_MINT}:
                raydium_type = "sell"

            return Raydium(
                type=raydium_type,
                who=instr.who,
                from_token=instr.from_token,
                from_amount=instr.from_token_amount / 10**instr.from_token_decimals,
                to_token=instr.to_token,
                to_amount=instr.to_token_amount / 10**instr.to_token_decimals,
                minimum_amount_out=instr.minimum_amount_out / 10**instr.to_token_decimals,
            )


RaydiumResolver = _RaydiumResolver()
