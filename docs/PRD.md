# PRD: DQN Stock Trading Learning Project

## Goal
Build an educational software project that demonstrates how daily stock data becomes a Reinforcement Learning problem solved by DQN. The goal is not financial advice and not next-day price prediction. The system learns a policy over `SELL`, `HOLD`, and `BUY` actions from states, actions, rewards, and future value estimates.

## Users and Success Criteria
- Primary reader: RL course evaluator who needs to inspect code, tests, architecture, and explanations.
- Secondary user: student running the project locally through CLI or Tkinter GUI.
- Acceptance criteria: reproducible data pipeline, `(N, 30, 10)` state tensor, Dueling DQN with replay and target network, reward comparison experiment, automated tests, Ruff configuration, and full README.

## Functional Requirements
- Download daily OHLCV data from Yahoo Finance through `yfinance`.
- Cache data as snappy parquet and fall back to CSV when network access fails.
- Create ten required features and chronological train/validation/test split.
- Train a Dueling DQN policy with epsilon-greedy exploration.
- Save checkpoints, metrics, and experiment outputs under `results/`.
- Provide Tkinter GUI and CLI commands through the SDK facade.

## Non-Functional Requirements
- Layered OOP architecture with no training logic inside GUI.
- Versioned configuration files and no hardcoded experiment parameters.
- Tests for data, features, environment, replay, model, training, checkpoint, and SDK.
- Python files should remain short and single-purpose where practical.
