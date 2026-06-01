# PRD: Data Pipeline

## Requirement
The project must reproduce the assignment dataset process: Yahoo Finance daily OHLCV data through `yfinance`, parquet cache under `data/raw/`, and CSV fallback.

## Inputs and Outputs
- Input: ticker, start date, end date, interval.
- Raw output: sorted `Open`, `High`, `Low`, `Close`, `Volume` table.
- Feature output: ten normalized channels and rolling state windows.

## Acceptance Tests
- Missing OHLCV columns raise a clear error.
- Offline mode loads `data/raw/{ticker}.csv`.
- Chronological split preserves temporal order and does not shuffle.
- Window output has shape `(N, 30, 10)`.
