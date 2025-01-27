# Parser instruction-name constants

# Generic
INSTR_UNKNOWN = "Unknown"

# Token program
INSTR_INITIALIZE_ACCOUNT = "InitializeAccount"
INSTR_TRANSFER = "Transfer"
INSTR_TRANSFER_CHECKED = "TransferChecked"

# System program
INSTR_TRANSFER_SOL = "Transfer"  # same name as token transfer, but used in system program
INSTR_CREATE_ACCOUNT_WITH_SEED = "CreateAccountWithSeed"

# Compute budget
INSTR_SET_COMPUTE_UNIT_LIMIT = "SetComputeUnitLimit"
INSTR_SET_COMPUTE_UNIT_PRICE = "SetComputeUnitPrice"

# Raydium
INSTR_SWAP = "Swap"

# PumpFun
INSTR_CREATE = "Create"
INSTR_BUY = "Buy"
INSTR_SELL = "Sell"