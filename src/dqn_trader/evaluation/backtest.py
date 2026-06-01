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
    actions: list[int]
    total_return: float
    max_drawdown: float
    win_rate: float


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
        drawdown = returns - np.maximum.accumulate(returns)
        return BacktestResult(equity, actions, float(returns[-1]), float(drawdown.min()), wins / max(len(actions), 1))

    @staticmethod
    def save(result: BacktestResult, results_dir: Path) -> None:
        results_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "total_return": result.total_return,
            "max_drawdown": result.max_drawdown,
            "win_rate": result.win_rate,
            "actions": result.actions,
        }
        (results_dir / "backtest_metrics.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
        plt.figure(figsize=(8, 4))
        plt.plot(result.equity_curve, label="DQN equity")
        plt.legend()
        plt.tight_layout()
        plt.savefig(results_dir / "backtest_equity.png")
        plt.close()


class InferenceService:
    @staticmethod
    def predict(model: DuelingDQNNetwork, state: np.ndarray) -> tuple[int, list[float]]:
        with torch.no_grad():
            q_values = model(torch.tensor(state[None, ...], dtype=torch.float32)).squeeze(0)
        return int(torch.argmax(q_values).item()), [float(value) for value in q_values]
