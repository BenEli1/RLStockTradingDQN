# Version History

## 1.00
- Created SDK-based DQN trading project.
- Added Yahoo Finance data client with parquet cache and CSV fallback.
- Added feature engineering for the required ten channels.
- Added Gymnasium-like trading environment.
- Added Dueling DQN, replay buffer, target network, training loop, checkpoints, and plots.
- Added backtest and prediction flows with CLI and Tkinter GUI.
- Added documentation, PRDs, Mermaid diagrams, tests, Ruff configuration, and `uv.lock`.

## Audit Improvement Pass
- Added Buy-and-Hold, Sharpe ratio, and trade count to backtest output.
- Added AI workflow, cost/resource analysis, version history, and experiment-summary documentation.
- Clarified limitations and avoided claiming unrun experiment results.

## Submission Evidence Pass
- Added readable training charts with per-episode loss aggregation.
- Added executable-action masking for backtest and latest prediction.
- Added one-click GUI pipeline through `TradingSDK.run_pipeline()`.
- Added raw-price validation with `auto_adjust=False` and `_raw.parquet` cache naming.
- Added assessment coverage, AI chat/process log, and source-control evidence documentation.
- Raised automated test coverage to 96.07% with 25 passing tests.
