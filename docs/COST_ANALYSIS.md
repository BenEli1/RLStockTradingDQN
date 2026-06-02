# Cost and Resource Analysis

## Direct API Costs
Yahoo Finance access through `yfinance` has no direct API-key cost for this coursework use. No secrets are required.

## Local Compute
Training runs locally with PyTorch. The default configuration is intentionally small (`episodes: 5`, compact MLP) so it can run on CPU. Increasing episodes, tickers, or model size will increase runtime.

Approximate resource profile for the submitted configuration:

| Resource | Current Project Choice | Cost Awareness |
|---|---|---|
| Training episodes | 5 by default | Keeps demos short for coursework and avoids long CPU runs. |
| Model | Compact Dueling DQN MLP | Avoids GPU requirement. |
| Data frequency | Daily OHLCV | Much cheaper than intraday data in storage and compute. |
| Tickers | AAPL plus comparison attempts | Small scope keeps experiments readable and reproducible. |
| Checkpoints | One best model path by default | Prevents unbounded checkpoint growth. |

## Storage
- Parquet cache files are stored under `data/raw/`.
- Checkpoints and generated plots are stored under `results/`.
- `.gitignore` excludes large generated outputs so the GitHub repository stays lightweight.
- Small experiment plots and metrics are committed because they are useful grading evidence.
- Model checkpoint `.pt` files are intentionally not committed because they can become large and are reproducible.

## AI Development Cost
AI tools were used as development assistance. Exact token counts are not available in the repository, so no fabricated token-cost table is included.

The professional cost decision here is transparency: AI assistance reduced implementation time, but the output still required review, tests, documentation, and correction. The repository therefore records AI workflow evidence without inventing exact token invoices.

## Operational Risks
- Free data sources can fail because of rate limits, TLS/certificate issues, or API changes.
- Running many tickers or long hyperparameter sweeps would require structured experiment tracking and possibly GPU compute.
- Large caches and checkpoints should be pruned or stored outside Git.
- Live trading would require paid data, compliance review, broker integration, risk controls, and monitoring. This project does none of that and is educational only.

## Scaling Considerations
Training many tickers or running hyperparameter sweeps would require stronger experiment tracking, larger storage budgets, and possibly GPU acceleration.
