from soltxs.parser.addons.platform_identifier import enrich
from soltxs.normalizer.models import LoadedAddresses, Message, Meta, Transaction


def test_enrichment_platform_identifier():
    """
    Ensures that if the transaction references a known platform address,
    it is properly identified.
    """
    tx = Transaction(
        slot=12345,
        blockTime=None,
        signatures=[],
        message=Message(
            accountKeys=[
                "RandomKey",
                "9RYJ3qr5eU5xAooqVcbmdeusjcViL5Nkiq7Gske3tiKq",  # known BullX address
            ],
            recentBlockhash="SomeBlockhash",
            instructions=[],
            addressTableLookups=[],
        ),
        meta=Meta(
            fee=0,
            preBalances=[],
            postBalances=[],
            preTokenBalances=[],
            postTokenBalances=[],
            innerInstructions=[],
            logMessages=[],
            err=None,
            status={},
            computeUnitsConsumed=None,
        ),
        loadedAddresses=LoadedAddresses(writable=[], readonly=[]),
    )

    platform_addr, platform_name = enrich(tx)
    assert platform_name == "BullX"
    assert platform_addr == "9RYJ3qr5eU5xAooqVcbmdeusjcViL5Nkiq7Gske3tiKq"


def test_enrichment_platform_not_found():
    """
    Ensures that if the transaction does not reference a known platform address,
    we get (None, None).
    """
    tx = Transaction(
        slot=0,
        blockTime=None,
        signatures=[],
        message=Message(
            accountKeys=["RandomKey1", "RandomKey2"],
            recentBlockhash="SomeBlockhash",
            instructions=[],
            addressTableLookups=[],
        ),
        meta=Meta(
            fee=0,
            preBalances=[],
            postBalances=[],
            preTokenBalances=[],
            postTokenBalances=[],
            innerInstructions=[],
            logMessages=[],
            err=None,
            status={},
            computeUnitsConsumed=None,
        ),
        loadedAddresses=LoadedAddresses(writable=[], readonly=[]),
    )

    platform_addr, platform_name = enrich(tx)
    assert platform_name is None
    assert platform_addr is None
