from dataclasses import dataclass
from typing import List, Optional

from soltxs import parser
from soltxs.resolver.models import Resolve, Resolver
from soltxs.constants import TREAT_AS_SOL, BUY, SELL




@dataclass(slots=True)
class Raydium(Resolve):
    type: str
    who: str
    from_token: str
    from_amount: float
    to_token: str
    to_amount: float
    minimum_amount_out: float


class _RaydiumResolver(Resolver):
    def resolve(self, instructions: List[parser.models.ParsedInstruction]) -> Optional[Resolve]:
        # We'll look for exactly one Raydium swap instruction.
        instrs = [i for i in instructions if isinstance(i, parser.parsers.raydiumAMM.Swap)]
        if len(instrs) == 1:
            instr = instrs[0]

            # If to_token is in TREAT_AS_SOL => user ended with more SOL => SELL
            # Else if from_token is in TREAT_AS_SOL => user spent SOL => BUY
            if instr.to_token in TREAT_AS_SOL:
                direction = SELL
            elif instr.from_token in TREAT_AS_SOL:
                direction = BUY
            else:
                # If neither is in TREAT_AS_SOL, fallback or default
                direction = BUY

            return Raydium(
                type=direction,
                who=instr.who,
                from_token=instr.from_token,
                from_amount=instr.from_token_amount / 10**instr.from_token_decimals,
                to_token=instr.to_token,
                to_amount=instr.to_token_amount / 10**instr.to_token_decimals,
                minimum_amount_out=instr.minimum_amount_out / 10**instr.to_token_decimals,
            )

        return None


RaydiumResolver = _RaydiumResolver()