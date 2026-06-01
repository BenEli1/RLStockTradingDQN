"""Gymnasium-style all-in/all-out stock trading environment."""

from dataclasses import dataclass

import numpy as np
import pandas as pd

from dqn_trader.env.reward import RewardFunction
from dqn_trader.shared.constants import FEATURE_COLUMNS, Action


@dataclass
class TradingEnv:
    features: pd.DataFrame
    prices: pd.Series
    window_size: int
    reward_function: RewardFunction
    initial_cash: float = 10000.0
    invalid_action_penalty: float = 0.01

    def reset(self) -> np.ndarray:
        self.index = self.window_size
        self.cash = float(self.initial_cash)
        self.shares = 0.0
        self.entry_price = 0.0
        self.done = False
        return self._state()

    def step(self, action: int) -> tuple[np.ndarray, float, bool, dict[str, float]]:
        previous_value = self._portfolio_value()
        price = float(self.prices.iloc[self.index])
        traded = False
        penalty = 0.0
        if action == Action.BUY and self.shares == 0:
            self.shares = self.cash / price
            self.cash = 0.0
            self.entry_price = price
            traded = True
        elif action == Action.SELL and self.shares > 0:
            self.cash = self.shares * price
            self.shares = 0.0
            traded = True
        elif action in (Action.BUY, Action.SELL):
            penalty = self.invalid_action_penalty
        self.index += 1
        self.done = self.index >= len(self.features) - 1
        current_value = self._portfolio_value()
        volatility = float(
            self.features["log_return"].iloc[max(0, self.index - 5) : self.index].std()
        )
        reward = (
            self.reward_function.compute(previous_value, current_value, traded, volatility)
            - penalty
        )
        return (
            self._state(),
            reward,
            self.done,
            {"portfolio_value": current_value, "traded": float(traded)},
        )

    def _portfolio_value(self) -> float:
        price = float(self.prices.iloc[min(self.index, len(self.prices) - 1)])
        return self.cash + self.shares * price

    def _state(self) -> np.ndarray:
        window = self.features.iloc[self.index - self.window_size : self.index].copy()
        price = float(self.prices.iloc[self.index])
        window.loc[:, "position"] = 1.0 if self.shares > 0 else 0.0
        window.loc[:, "unrealised_pnl"] = (
            0.0 if self.shares == 0 else (price - self.entry_price) / self.entry_price
        )
        return window[FEATURE_COLUMNS].to_numpy(dtype=np.float32)
