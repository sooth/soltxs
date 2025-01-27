from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from soltxs.normalizer.models import Transaction
from soltxs.parser.models import ParsedInstruction, Program
from soltxs.parser.parsers.constants import (
    INSTR_SET_COMPUTE_UNIT_LIMIT,
    INSTR_SET_COMPUTE_UNIT_PRICE,
)


@dataclass(slots=True)
class SetComputeUnitLimit(ParsedInstruction):
    compute_unit_limit: int


@dataclass(slots=True)
class SetComputeUnitPrice(ParsedInstruction):
    micro_lamports: int


ParsedInstructions = Union[SetComputeUnitLimit, SetComputeUnitPrice]


class _ComputeBudgetParser(Program[ParsedInstructions]):
    """
    Solana's Compute Budget program for adjusting compute unit limits and prices.
    """

    def __init__(self):
        self.program_id = "ComputeBudget111111111111111111111111111111"
        self.program_name = "ComputeBudget"

        self.desc = lambda d: d[0]
        self.desc_map = {
            2: self.process_SetComputeUnitLimit,
            3: self.process_SetComputeUnitPrice,
        }

    def process_SetComputeUnitLimit(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
    ) -> SetComputeUnitLimit:
        return SetComputeUnitLimit(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name=INSTR_SET_COMPUTE_UNIT_PRICE,
            compute_unit_limit=int.from_bytes(decoded_data[1:5], byteorder="little", signed=False),
        )

    def process_SetComputeUnitPrice(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
    ) -> SetComputeUnitPrice:
        return SetComputeUnitPrice(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="SetComputeUnitPrice",
            micro_lamports=int.from_bytes(decoded_data[1:9], byteorder="little", signed=False),
        )


ComputeBudgetParser = _ComputeBudgetParser()