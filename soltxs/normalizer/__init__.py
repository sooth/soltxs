from soltxs.normalizer import models, normalizers


def normalize(data: dict) -> models.Transaction:
    """
    Standardizes a Solana transaction response.
    """
    if "jsonrpc" in data and "result" in data:
        return normalizers.rpc.normalize(data)
    elif "transaction" in data and "transaction" in data["transaction"]:
        return normalizers.geyser.normalize(data)

    raise ValueError("Unrecognized Solana transaction format.")
