"""Experience replay buffer."""

from collections import deque
from dataclasses import dataclass
from random import sample

import numpy as np


@dataclass(frozen=True)
class Transition:
    state: np.ndarray
    action: int
    reward: float
    next_state: np.ndarray
    done: bool


class ReplayBuffer:
    def __init__(self, capacity: int) -> None:
        self._buffer: deque[Transition] = deque(maxlen=capacity)

    def push(self, transition: Transition) -> None:
        self._buffer.append(transition)

    def sample(self, batch_size: int) -> list[Transition]:
        if batch_size > len(self._buffer):
            raise ValueError("Cannot sample more transitions than are stored")
        return sample(list(self._buffer), batch_size)

    def __len__(self) -> int:
        return len(self._buffer)
