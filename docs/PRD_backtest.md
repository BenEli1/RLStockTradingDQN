# PRD: Backtest and Evaluation

## Requirement
Evaluation must be separate from training exploration. Backtest uses greedy Q-value action selection, not epsilon-random exploration.

## Metrics
- DQN equity curve.
- Buy-and-Hold baseline.
- Total return.
- Buy-and-Hold return.
- Sharpe ratio.
- Max drawdown.
- Win rate.
- Number of non-hold trades.

## Output
When backtest is run, the system writes `results/backtest_metrics.json` and `results/backtest_equity.png`.

## Limitation
Backtest is an educational diagnostic, not proof of future trading performance.
