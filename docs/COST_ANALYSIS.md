# Cost and Resource Analysis

## Direct API Costs
Yahoo Finance access through `yfinance` has no direct API-key cost for this coursework use. No secrets are required.

## Local Compute
Training runs locally with PyTorch. The default configuration is intentionally small (`episodes: 5`, compact MLP) so it can run on CPU. Increasing episodes, tickers, or model size will increase runtime.

## Storage
- Parquet cache files are stored under `data/raw/`.
- Checkpoints and generated plots are stored under `results/`.
- `.gitignore` excludes large generated outputs so the GitHub repository stays lightweight.

## AI Development Cost
AI tools were used as development assistance. Exact token counts are not available in the repository, so no fabricated token-cost table is included.

## Scaling Considerations
Training many tickers or running hyperparameter sweeps would require stronger experiment tracking, larger storage budgets, and possibly GPU acceleration.
