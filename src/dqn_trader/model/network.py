"""Dueling DQN network."""

import torch
from torch import nn


class DuelingDQNNetwork(nn.Module):
    def __init__(self, window_size: int, feature_count: int, action_count: int = 3) -> None:
        super().__init__()
        input_size = window_size * feature_count
        self.encoder = nn.Sequential(nn.Flatten(), nn.Linear(input_size, 128), nn.ReLU(), nn.Linear(128, 64), nn.ReLU())
        self.value = nn.Sequential(nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, 1))
        self.advantage = nn.Sequential(nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, action_count))

    def forward(self, states: torch.Tensor) -> torch.Tensor:
        encoded = self.encoder(states)
        value = self.value(encoded)
        advantage = self.advantage(encoded)
        return value + advantage - advantage.mean(dim=1, keepdim=True)
