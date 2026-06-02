# Results Summary

Real compact reward-comparison output was generated with:

```powershell
uv run python scripts/run_experiments.py
```

See:

- `results/experiments/REPORT.md`
- `results/experiments/summary.json`
- `results/experiments/aapl_risk_adjusted/`
- `results/experiments/aapl_basic_reward/`

The attempted `SPY` run in the first reward-comparison script failed locally because yfinance/curl could not verify the TLS certificate. That historical failure is documented in the report. After adding the Yahoo Chart API fallback, the broader 10-stock research pass completed successfully and is documented in `results/multi_stock/REPORT.md`.

Do not interpret generated backtest values as financial advice or evidence of future trading performance.
