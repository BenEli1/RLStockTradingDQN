"""DQN training service."""

import json
import random as random_module
from dataclasses import dataclass
from pathlib import Path
from random import random, randrange

import matplotlib.pyplot as plt
import numpy as np
import torch
from torch import nn

from dqn_trader.env.trading_env import TradingEnv
from dqn_trader.memory.replay_buffer import ReplayBuffer, Transition
from dqn_trader.model.network import DuelingDQNNetwork


@dataclass
class TrainingResult:
    rewards: list[float]
    losses: list[float]
    checkpoint_path: Path


class TrainingService:
    def __init__(self, config: dict) -> None:
        self.config = config

    def train(self, env: TradingEnv, checkpoint_path: Path) -> TrainingResult:
        cfg = self.config
        random_module.seed(cfg.get("seed", 42))
        np.random.seed(cfg.get("seed", 42))
        torch.manual_seed(cfg.get("seed", 42))
        policy = DuelingDQNNetwork(env.window_size, 10)
        target = DuelingDQNNetwork(env.window_size, 10)
        target.load_state_dict(policy.state_dict())
        optimizer = torch.optim.Adam(policy.parameters(), lr=cfg["learning_rate"])
        buffer = ReplayBuffer(cfg["replay_capacity"])
        epsilon = cfg["epsilon_start"]
        rewards, losses, best_reward = [], [], -float("inf")
        for _episode in range(cfg["episodes"]):
            state = env.reset()
            total_reward = 0.0
            steps = 0
            while True:
                action = randrange(3) if random() < epsilon else self._select(policy, state)
                next_state, reward, done, _info = env.step(action)
                buffer.push(Transition(state, action, reward, next_state, done))
                state, total_reward = next_state, total_reward + reward
                if len(buffer) >= cfg["batch_size"]:
                    losses.append(self._learn(policy, target, optimizer, buffer))
                steps += 1
                if steps % cfg["target_update_steps"] == 0:
                    target.load_state_dict(policy.state_dict())
                if done:
                    break
            epsilon = max(cfg["epsilon_end"], epsilon * cfg["epsilon_decay"])
            if total_reward > best_reward:
                best_reward = total_reward
                checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
                torch.save(
                    {"model_state": policy.state_dict(), "reward": total_reward}, checkpoint_path
                )
            rewards.append(total_reward)
        self._write_metrics(checkpoint_path.parent, rewards, losses)
        return TrainingResult(rewards, losses, checkpoint_path)

    def _learn(
        self,
        policy: nn.Module,
        target: nn.Module,
        optimizer: torch.optim.Optimizer,
        buffer: ReplayBuffer,
    ) -> float:
        batch = buffer.sample(self.config["batch_size"])
        states = torch.tensor(np.stack([t.state for t in batch]), dtype=torch.float32)
        actions = torch.tensor([t.action for t in batch], dtype=torch.long).unsqueeze(1)
        rewards = torch.tensor([t.reward for t in batch], dtype=torch.float32)
        next_states = torch.tensor(np.stack([t.next_state for t in batch]), dtype=torch.float32)
        dones = torch.tensor([t.done for t in batch], dtype=torch.float32)
        q_values = policy(states).gather(1, actions).squeeze(1)
        with torch.no_grad():
            targets = rewards + self.config["gamma"] * target(next_states).max(1).values * (
                1 - dones
            )
        loss = nn.functional.huber_loss(q_values, targets)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        return float(loss.item())

    @staticmethod
    def _select(policy: nn.Module, state: np.ndarray) -> int:
        with torch.no_grad():
            q_values = policy(torch.tensor(state[None, ...], dtype=torch.float32))
        return int(torch.argmax(q_values, dim=1).item())

    @staticmethod
    def _write_metrics(results_dir: Path, rewards: list[float], losses: list[float]) -> None:
        results_dir.mkdir(parents=True, exist_ok=True)
        (results_dir / "training_metrics.json").write_text(
            json.dumps({"rewards": rewards, "losses": losses}, indent=2),
            encoding="utf-8",
        )
        plt.figure(figsize=(8, 4))
        plt.plot(rewards, label="episode reward")
        if losses:
            plt.plot(losses, label="loss", alpha=0.7)
        plt.legend()
        plt.tight_layout()
        plt.savefig(results_dir / "training_curve.png")
        plt.close()
