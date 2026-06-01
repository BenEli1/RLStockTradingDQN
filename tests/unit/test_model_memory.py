import numpy as np
import pytest
import torch

from dqn_trader.memory.replay_buffer import ReplayBuffer, Transition
from dqn_trader.model.network import DuelingDQNNetwork


def test_dueling_network_forward_shape():
    network = DuelingDQNNetwork(30, 10)
    output = network(torch.zeros((4, 30, 10)))
    assert output.shape == (4, 3)


def test_replay_buffer_sample():
    buffer = ReplayBuffer(10)
    state = np.zeros((30, 10), dtype=np.float32)
    buffer.push(Transition(state, 1, 0.5, state, False))
    assert len(buffer.sample(1)) == 1
    with pytest.raises(ValueError):
        buffer.sample(2)
