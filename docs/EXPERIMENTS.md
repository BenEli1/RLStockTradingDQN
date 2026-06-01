# Experiment Summary

Real compact local experiments were run with:

```powershell
uv run python scripts/run_experiments.py
```

The full generated report is committed at `results/experiments/REPORT.md`. The runs are educational diagnostics only, not financial advice.

## Controlled Comparison

| Item | Setup |
|---|---|
| Hypothesis | Cost/risk-adjusted rewards reduce unstable over-trading compared with a basic portfolio-delta reward. |
| Main ticker | AAPL, 2020-01-01 to 2023-01-01, interval 1d |
| Attempted comparison ticker | SPY, same date range and data mechanism |
| Completed comparison | AAPL risk-adjusted reward vs AAPL basic reward |
| Model | Dueling DQN with regular replay and target network |
| Metrics | Total return, Buy-and-Hold return, Sharpe ratio, max drawdown, win rate, trade count |

## Results

| Run | Ticker | Reward | Episodes | DQN Return | Buy/Hold Return | Sharpe | Max Drawdown | Win Rate | Trades |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aapl_risk_adjusted | AAPL | risk_adjusted | 5 | 1.0678 | 0.8993 | 0.9478 | -0.3035 | 0.4773 | 25 |
| aapl_basic_reward | AAPL | basic | 5 | 2.4318 | 0.8993 | 1.7794 | -0.2356 | 0.3229 | 79 |
| spy_risk_adjusted | SPY | risk_adjusted | 5 | failed | failed | failed | failed | failed | failed |

## Output Files

- `results/experiments/REPORT.md`
- `results/experiments/summary.json`
- Per-run training metrics, training curves, backtest metrics, and equity plots.

## Critical Conclusion

The short runs demonstrate that the code path works end-to-end, but they are not enough to claim a robust trading policy. The basic reward traded more often than the risk-adjusted reward, which supports the assignment's warning that reward design affects behavior. SPY failed locally because yfinance/curl could not verify the TLS certificate; this should be rerun with working network certificates or a CSV fallback.
