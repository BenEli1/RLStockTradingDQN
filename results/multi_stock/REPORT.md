# Multi-Stock Research Report

This report runs the same Dueling DQN pipeline across a broader set of well-known stocks and one ETF.
The purpose is research coverage and robustness evidence, not financial advice or proof of future profitability.

Command:

```powershell
uv run python scripts/run_multi_stock_research.py
```

Setup: daily Yahoo Finance/yfinance OHLCV, 2020-01-01 to 2023-01-01, chronological data, risk-adjusted reward, compact CPU-friendly training.

| Ticker | Company / Asset | Sector | Status | DQN Return | Buy/Hold | Sharpe | Max Drawdown | Trades | Prediction |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| AAPL | Apple | Technology | ok | 0.9202 | 0.8651 | 0.8880 | -0.3075 | 9 | BUY |
| NVDA | NVIDIA | Semiconductors / AI | ok | 6.6081 | 1.4253 | 1.8983 | -0.3521 | 250 | HOLD |
| NFLX | Netflix | Streaming media | ok | -0.0966 | -0.1343 | 0.1755 | -0.7248 | 23 | HOLD |
| META | Meta Platforms | Social media | ok | -0.1689 | -0.2938 | 0.0837 | -0.7368 | 77 | HOLD |
| SPY | S&P 500 ETF | Market ETF | ok | 1.3913 | 0.4237 | 2.0071 | -0.0964 | 178 | BUY |
| AMZN | Amazon | E-commerce / cloud | ok | 0.3786 | -0.0568 | 0.4958 | -0.4694 | 53 | HOLD |
| MCD | McDonald's | Consumer staples / restaurants | ok | 0.1662 | 0.5013 | 0.5144 | -0.0767 | 6 | HOLD |
| KO | Coca-Cola | Consumer staples | ok | 1.6473 | 0.3194 | 1.8672 | -0.1783 | 236 | BUY |
| CRWD | CrowdStrike | Cybersecurity | ok | 1.5637 | 1.6440 | 0.8651 | -0.6590 | 5 | BUY |
| PFE | Pfizer | Healthcare / pharmaceuticals | ok | 1.3866 | 0.6540 | 1.6787 | -0.1975 | 99 | BUY |

## Interpretation

- This broad run checks whether the implementation can execute across different market regimes and sectors.
- The model and episode count are intentionally compact for coursework timing, so the results should be read as engineering evidence rather than trading claims.
- Buy-and-Hold remains the baseline because a DQN return is only meaningful when compared against a passive strategy on the same ticker and period.
- Differences in trade count, drawdown, and Sharpe show that reward and market behavior interact differently across assets.
