"""Shared constants for the trading domain."""

from enum import IntEnum


class Action(IntEnum):
    SELL = 0
    HOLD = 1
    BUY = 2


FEATURE_COLUMNS = [
    "log_return",
    "rsi_14",
    "macd",
    "macd_signal",
    "macd_hist",
    "bb_pct",
    "vwap_dist",
    "volume_norm",
    "position",
    "unrealised_pnl",
]

RAW_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]
