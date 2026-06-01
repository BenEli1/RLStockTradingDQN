# Experiment Summary

No real AAPL/SPY experiment results are committed yet. This is intentional: fabricated metrics would be misleading. Run the commands below after dependency setup and network access, or after placing CSV fallback files in `data/raw/`.

## Planned Controlled Comparison

| Item | Setup |
|---|---|
| Hypothesis | Cost/risk-adjusted rewards reduce unstable over-trading compared with a basic portfolio-delta reward. |
| Main ticker | AAPL, 2020-01-01 to 2023-01-01, interval 1d |
| Comparison ticker | SPY, same date range and data mechanism |
| Model | Dueling DQN with regular replay and target network |
| Metrics | Total return, Buy-and-Hold return, Sharpe ratio, max drawdown, win rate, trade count |

## Commands

```powershell
uv sync --extra dev
uv run dqn-trader train --ticker AAPL
uv run dqn-trader backtest --ticker AAPL
uv run dqn-trader train --ticker SPY
uv run dqn-trader backtest --ticker SPY
```

## Expected Output Files

- `results/training_metrics.json`
- `results/training_curve.png`
- `results/backtest_metrics.json`
- `results/backtest_equity.png`

## Critical Conclusion Template

After running the experiments, report whether the policy traded too often, whether Sharpe and drawdown support or contradict total return, and whether behavior on SPY suggests any generalization beyond AAPL.
