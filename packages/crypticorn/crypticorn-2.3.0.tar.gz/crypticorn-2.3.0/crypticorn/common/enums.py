from enum import StrEnum


class Exchange(StrEnum):
    """Supported exchanges for trading"""

    KUCOIN = "kucoin"
    BINGX = "bingx"


class InternalExchange(StrEnum):
    """All exchanges we are using, including public (Exchange)"""

    KUCOIN = "kucoin"
    BINGX = "bingx"
    BINANCE = "binance"
    BYBIT = "bybit"
    HYPERLIQUID = "hyperliquid"
    BITGET = "bitget"


class MarketType(StrEnum):
    """
    Market types
    """

    SPOT = "spot"
    FUTURES = "futures"
