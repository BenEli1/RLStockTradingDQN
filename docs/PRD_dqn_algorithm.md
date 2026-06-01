# PRD: Dueling DQN Algorithm

## Requirement
The model must be a real DQN learner, not a supervised price predictor. It estimates action values and learns from `(s, a, r, s', done)` transitions.

## Design
- `DuelingDQNNetwork` returns three Q-values.
- `ReplayBuffer` stores transitions and samples mini-batches.
- `TrainingService` computes Bellman targets with a target network.
- Epsilon-greedy exploration is used during training.

## Acceptance Tests
- Forward pass shape is `(batch, 3)`.
- Replay buffer rejects over-sampling.
- Training writes a checkpoint.
