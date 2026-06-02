# Experiment Summary

Real compact local experiments were run in two layers. First, a controlled reward-comparison run was generated with:

```powershell
uv run python scripts/run_experiments.py
```

The generated reward-comparison report is committed at `results/experiments/REPORT.md`. The runs are educational diagnostics only, not financial advice.

## Controlled Comparison

| Item | Setup |
|---|---|
| Hypothesis | Cost/risk-adjusted rewards reduce unstable over-trading compared with a basic portfolio-delta reward. |
| Main ticker | AAPL, 2020-01-01 to 2023-01-01, interval 1d |
| Initial network-stress ticker | SPY, same date range and data mechanism |
| Completed comparison | AAPL risk-adjusted reward vs AAPL basic reward |
| Model | Dueling DQN with regular replay and target network |
| Metrics | Total return, Buy-and-Hold return, Sharpe ratio, max drawdown, win rate, trade count |

## Results

| Run | Ticker | Reward | Episodes | DQN Return | Buy/Hold Return | Sharpe | Max Drawdown | Win Rate | Trades |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aapl_risk_adjusted | AAPL | risk_adjusted | 5 | 1.0678 | 0.8993 | 0.9478 | -0.3035 | 0.4773 | 23 |
| aapl_basic_reward | AAPL | basic | 5 | 2.4318 | 0.8993 | 1.7794 | -0.2356 | 0.3244 | 63 |
| spy_risk_adjusted | SPY | risk_adjusted | 5 | failed in this early run | failed | failed | failed | failed | failed |

## Output Files

- `results/experiments/REPORT.md`
- `results/experiments/summary.json`
- Per-run training metrics, training curves, backtest metrics, and equity plots.

## Critical Conclusion

The short runs demonstrate that the code path works end-to-end, but they are not enough to claim a robust trading policy. The basic reward traded more often than the risk-adjusted reward, which supports the assignment's warning that reward design affects behavior. The early SPY run failed because yfinance/curl could not verify the TLS certificate; that failure led to the Yahoo Chart API fallback used successfully in the later multi-stock pass.

## Multi-Stock Research Pass

A broader research pass was added with:

```powershell
uv run python scripts/run_multi_stock_research.py
```

The report is committed at `results/multi_stock/REPORT.md`. This later pass completed all ten symbols, including SPY, using the improved Yahoo Finance data fallback.

This pass runs the same Dueling DQN pipeline on:

| Ticker | Company / Asset | Sector |
|---|---|---|
| AAPL | Apple | Technology |
| NVDA | NVIDIA | Semiconductors / AI |
| NFLX | Netflix | Streaming media |
| META | Meta Platforms | Social media |
| SPY | S&P 500 ETF | Market ETF |
| AMZN | Amazon | E-commerce / cloud |
| MCD | McDonald's | Consumer staples / restaurants |
| KO | Coca-Cola | Consumer staples |
| CRWD | CrowdStrike | Cybersecurity |
| PFE | Pfizer | Healthcare / pharmaceuticals |

The multi-stock pass uses compact three-episode runs, so it is research coverage and engineering evidence rather than a profitability claim. It was useful because the same implementation had to handle different volatility profiles, sectors, and return histories.
