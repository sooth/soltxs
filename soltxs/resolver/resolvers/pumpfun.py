from dataclasses import dataclass
from typing import List, Optional

from soltxs import parser
from soltxs.resolver.models import Resolve, Resolver
from soltxs.constants import TREAT_AS_SOL, BUY, SELL


@dataclass(slots=True)
class PumpFun(Resolve):
    type: str
    who: str
    from_token: str
    from_amount: float
    to_token: str
    to_amount: float


class _PumpFunResolver(Resolver):
    def resolve(self, instructions: List[parser.models.ParsedInstruction]) -> Optional[Resolve]:
        # We look for exactly one PumpFun (Buy or Sell) instruction.
        instrs = [i for i in instructions if isinstance(i, (parser.parsers.pumpfun.Buy, parser.parsers.pumpfun.Sell))]
        if len(instrs) == 1:
            instr = instrs[0]

            # TREAT_AS_SOL logic:
            # if to_token is in TREAT_AS_SOL => SELL
            # else if from_token is in TREAT_AS_SOL => BUY
            if instr.to_token in TREAT_AS_SOL:
                direction = SELL
            elif instr.from_token in TREAT_AS_SOL:
                direction = BUY
            else:
                # If neither is TREAT_AS_SOL, fallback
                direction = BUY

            return PumpFun(
                type=direction,
                who=instr.who,
                from_token=instr.from_token,
                from_amount=instr.from_token_amount / 10**instr.from_token_decimals,
                to_token=instr.to_token,
                to_amount=instr.to_token_amount / 10**instr.to_token_decimals,
            )

        return None


PumpFunResolver = _PumpFunResolver()