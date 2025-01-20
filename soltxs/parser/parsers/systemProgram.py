from dataclasses import dataclass
from typing import Optional, Union

import qborsh

from soltxs.normalizer.models import Instruction, Transaction
from soltxs.parser.models import ParsedInstruction, Program


@dataclass(slots=True)
class Transfer(ParsedInstruction):
    from_account: Optional[str]
    to_account: Optional[str]
    lamports: int


@dataclass(slots=True)
class createAccount(ParsedInstruction):
    who: Optional[str]
    new_account: Optional[str]
    base: str
    seed: str
    lamports: int
    space: int
    owner: str


ParsedInstructions = Union[Transfer, createAccount]


class U64String(qborsh.BorshType):
    """
    Reads/writes a string with an 8-byte length prefix (uint64 LE).
    Followed by 'length' UTF-8 bytes.
    """

    def serialize(self, buf: qborsh.Buffer, value: str):
        if not isinstance(value, str):
            raise TypeError("U64String expects a string input.")
        encoded = value.encode("utf-8")
        length = len(encoded)
        buf.write_u64(length)
        buf.write_fixed_array(encoded)

    def deserialize(self, buf: qborsh.Buffer) -> str:
        length = buf.read_u64()
        raw = buf.read_fixed_array(length)
        return raw.decode("utf-8", errors="replace")

    def sizeof(self):
        return None


@qborsh.schema
class CreateAccountWithSeedData:
    discriminator: qborsh.Padding[qborsh.U32]
    base: qborsh.PubKey
    seed: U64String
    lamports: qborsh.U64
    space: qborsh.U64
    owner: qborsh.PubKey


@qborsh.schema
class TransferData:
    discriminator: qborsh.Padding[qborsh.U32]
    lamports: qborsh.U64


class _SystemProgramParser(Program[ParsedInstructions]):
    """
    System Program for account creation, transfers, and more.
    """

    def __init__(self):
        self.program_id = "11111111111111111111111111111111"
        self.program_name = "System Program"

        self.desc = lambda d: int.from_bytes(d[0:4], byteorder="little", signed=False)
        self.desc_map = {
            2: self.process_Transfer,
            3: self.process_CreateAccount,
        }

    def process_Transfer(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
    ) -> Transfer:
        instr: Instruction = tx.message.instructions[instruction_index]
        data = TransferData.decode(decoded_data)
        accounts = instr.accounts

        from_account = tx.all_accounts[accounts[0]] if len(accounts) > 0 else None
        to_account = tx.all_accounts[accounts[1]] if len(accounts) > 1 else None

        return Transfer(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="Transfer",
            from_account=from_account,
            to_account=to_account,
            lamports=int(data["lamports"]),
        )

    def process_CreateAccount(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
    ) -> createAccount:
        instr: Instruction = tx.message.instructions[instruction_index]
        accounts = instr.accounts

        parsed = CreateAccountWithSeedData.decode(decoded_data)

        who = tx.all_accounts[accounts[0]] if len(accounts) > 0 else None
        new_account = tx.all_accounts[accounts[1]] if len(accounts) > 1 else None

        return createAccount(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="CreateAccountWithSeed",
            who=who,
            new_account=new_account,
            base=parsed["base"],
            seed=parsed["seed"],
            lamports=parsed["lamports"],
            space=parsed["space"],
            owner=parsed["owner"],
        )


SystemProgramParser = _SystemProgramParser()
