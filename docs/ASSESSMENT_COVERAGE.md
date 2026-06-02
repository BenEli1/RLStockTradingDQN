# Assessment Coverage Matrix

This document maps the Homework 02 requirements and previous-feedback criteria to concrete repository evidence.

| Criterion | Status | Evidence |
|---|---|---|
| RL project, not stock-price prediction | Pass | `README.md`, `docs/RL_TUTORIAL.md` |
| Agent/environment/state/action/reward/episode/policy/return mapping | Pass | `README.md` RL Mapping table |
| Q-table to DQN explanation | Pass | `README.md`, `docs/RL_TUTORIAL.md` |
| Dueling DQN value/advantage explanation | Pass | `README.md`, `src/dqn_trader/model/network.py` |
| Gymnasium-like `reset()` / `step()` environment | Pass | `src/dqn_trader/env/trading_env.py`, tests |
| Three actions: Sell/Hold/Buy | Pass | `src/dqn_trader/shared/constants.py`, README |
| Invalid action handling | Pass | `TradingEnv.step()`, `tests/unit/test_env_reward.py` |
| 30 x 10 state tensor | Pass | `config/setup.yaml`, `FeatureEngineer`, tests |
| yfinance/Yahoo Finance data path | Pass with local TLS limitation | `YFinanceDataClient`; README limitation |
| AAPL 2020-01-01 to 2023-01-01 | Pass | `config/setup.yaml`, experiment report |
| SPY/NVDA comparison and broader research | Pass | `results/multi_stock/REPORT.md` includes SPY, NVDA, and eight additional assets |
| Parquet cache and CSV fallback | Pass | `YFinanceDataClient`, `tests/unit/test_data_client.py` |
| Raw OHLCV validation | Pass | `auto_adjust=False` test and README price note |
| Chronological split, no shuffle | Pass | `FeatureEngineer.chronological_split`, tests |
| Replay buffer and target network | Pass | `src/dqn_trader/memory/`, `TrainingService` |
| Epsilon-greedy exploration | Pass | `TrainingService`, `config/setup.yaml` |
| Backtest without random exploration | Pass | `BacktestService`, legal-action masking |
| Metrics: equity, Buy-and-Hold, return, Sharpe, drawdown, win rate, trades | Pass | `BacktestResult`, result JSONs |
| Controlled reward comparison | Pass | `docs/EXPERIMENTS.md`, `results/experiments/` |
| GUI demonstration | Pass | Tkinter GUI, `assets/`, README guide |
| SDK/facade architecture | Pass | `TradingSDK`, `docs/PLAN.md`, diagrams |
| README, PRD, PLAN, TODO | Pass | Root README and `docs/` |
| Configuration and security | Pass | `config/setup.yaml`, `.env-example`, `.gitignore` |
| AI workflow visibility | Pass | `docs/AI_WORKFLOW.md`, `docs/AI_CHAT_LOG.md` |
| Source control / version management | Pass | GitHub repo, `docs/SOURCE_CONTROL.md`, `docs/VERSION_HISTORY.md` |
| Cost/resource awareness | Pass | `docs/COST_ANALYSIS.md` |
| Extensibility | Pass | README Extension Points, `docs/PLAN.md` |
| Automated quality standards | Pass | Ruff, pytest, 25 tests, 96.07% coverage |

## Still Risky / Manual Review

- Live yfinance calls on this machine can fail because curl cannot verify the local certificate chain. The code now also supports a secondary Yahoo Chart API fallback plus CSV fallback.
- The experiments are intentionally short five-episode coursework diagnostics. They show pipeline behavior and reward-design effects, not a robust profitable trading strategy.
- The first GUI screenshot in the README is an actual completed local run. Real experiment plots are committed under `results/experiments/` and `results/multi_stock/`.
