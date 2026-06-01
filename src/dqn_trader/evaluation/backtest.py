"""Backtest and inference services."""

import json
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch

from dqn_trader.env.trading_env import TradingEnv
from dqn_trader.model.network import DuelingDQNNetwork


@dataclass
class BacktestResult:
    equity_curve: list[float]
    buy_hold_curve: list[float]
    actions: list[int]
    total_return: float
    buy_hold_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    trade_count: int


class BacktestService:
    def run(self, env: TradingEnv, model: DuelingDQNNetwork) -> BacktestResult:
        state = env.reset()
        equity, actions, wins = [], [], 0
        while True:
            action, _q_values = InferenceService.predict(model, state)
            state, reward, done, info = env.step(action)
            equity.append(info["portfolio_value"])
            actions.append(action)
            wins += int(reward > 0)
            if done:
                break
        returns = np.array(equity) / equity[0] - 1 if equity else np.array([0.0])
        equity_array = np.array(equity)
        running_peak = np.maximum.accumulate(equity_array)
        drawdown = (equity_array - running_peak) / running_peak
        buy_hold = self._buy_hold_curve(env, len(equity))
        buy_hold_return = buy_hold[-1] / buy_hold[0] - 1 if buy_hold else 0.0
        sharpe = self._sharpe(np.diff(np.array(equity)) / np.array(equity[:-1]))
        trade_count = sum(1 for action in actions if action != 1)
        return BacktestResult(
            equity,
            buy_hold,
            actions,
            float(returns[-1]),
            float(buy_hold_return),
            sharpe,
            float(drawdown.min()),
            wins / max(len(actions), 1),
            trade_count,
        )

    @staticmethod
    def save(result: BacktestResult, results_dir: Path) -> None:
        results_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "total_return": result.total_return,
            "buy_hold_return": result.buy_hold_return,
            "sharpe_ratio": result.sharpe_ratio,
            "max_drawdown": result.max_drawdown,
            "win_rate": result.win_rate,
            "trade_count": result.trade_count,
            "actions": result.actions,
        }
        (results_dir / "backtest_metrics.json").write_text(
            json.dumps(payload, indent=2), encoding="utf-8"
        )
        plt.figure(figsize=(8, 4))
        plt.plot(result.equity_curve, label="DQN equity")
        plt.plot(result.buy_hold_curve, label="Buy-and-Hold", alpha=0.75)
        plt.legend()
        plt.tight_layout()
        plt.savefig(results_dir / "backtest_equity.png")
        plt.close()

    @staticmethod
    def _buy_hold_curve(env: TradingEnv, length: int) -> list[float]:
        start = env.window_size
        prices = env.prices.iloc[start : start + length].to_numpy()
        if len(prices) == 0:
            return []
        shares = env.initial_cash / prices[0]
        return [float(shares * price) for price in prices]

    @staticmethod
    def _sharpe(step_returns: np.ndarray) -> float:
        if len(step_returns) == 0 or float(step_returns.std()) == 0.0:
            return 0.0
        return float(np.sqrt(252) * step_returns.mean() / step_returns.std())


class InferenceService:
    @staticmethod
    def predict(model: DuelingDQNNetwork, state: np.ndarray) -> tuple[int, list[float]]:
        with torch.no_grad():
            q_values = model(torch.tensor(state[None, ...], dtype=torch.float32)).squeeze(0)
        return int(torch.argmax(q_values).item()), [float(value) for value in q_values]
