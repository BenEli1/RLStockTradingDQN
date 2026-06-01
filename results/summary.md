# Results Summary

Real compact experiment output was generated with:

```powershell
uv run python scripts/run_experiments.py
```

See:

- `results/experiments/REPORT.md`
- `results/experiments/summary.json`
- `results/experiments/aapl_risk_adjusted/`
- `results/experiments/aapl_basic_reward/`

The attempted `SPY` run failed locally because yfinance/curl could not verify the TLS certificate. This is documented in the report.

Do not interpret generated backtest values as financial advice or evidence of future trading performance.
