"""Feature engineering and chronological window creation."""

from dataclasses import dataclass

import numpy as np
import pandas as pd

from dqn_trader.shared.constants import FEATURE_COLUMNS


@dataclass
class FeatureEngineer:
    window_size: int = 30

    def transform(self, raw: pd.DataFrame) -> pd.DataFrame:
        close = raw["Close"]
        volume = raw["Volume"]
        log_return = np.log(close / close.shift(1))
        delta = close.diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = (-delta.clip(upper=0)).rolling(14).mean()
        rs = gain / loss.replace(0, 1e-9)
        rsi = 100 - (100 / (1 + rs))
        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()
        middle = close.rolling(20).mean()
        std = close.rolling(20).std()
        bb_pct = (close - (middle - 2 * std)) / (4 * std)
        vwap = (raw["Close"] * volume).rolling(20).sum() / volume.rolling(20).sum()
        features = pd.DataFrame(index=raw.index)
        features["log_return"] = log_return
        features["rsi_14"] = rsi / 100
        features["macd"] = macd / close
        features["macd_signal"] = signal / close
        features["macd_hist"] = (macd - signal) / close
        features["bb_pct"] = bb_pct
        features["vwap_dist"] = (close - vwap) / close
        features["volume_norm"] = volume / volume.rolling(20).mean() - 1
        features["position"] = 0.0
        features["unrealised_pnl"] = 0.0
        return features.replace([np.inf, -np.inf], np.nan).dropna()

    def make_windows(self, features: pd.DataFrame) -> np.ndarray:
        values = features[FEATURE_COLUMNS].to_numpy(dtype=np.float32)
        if len(values) < self.window_size:
            raise ValueError("Not enough rows to create a state window")
        return np.stack([values[i : i + self.window_size] for i in range(len(values) - self.window_size + 1)])

    @staticmethod
    def chronological_split(frame: pd.DataFrame, train: float, validation: float) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        train_end = int(len(frame) * train)
        validation_end = train_end + int(len(frame) * validation)
        return frame.iloc[:train_end], frame.iloc[train_end:validation_end], frame.iloc[validation_end:]
