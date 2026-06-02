# AI Chat and Iteration Log

This file summarizes the AI-assisted development conversation for transparency. It is not a raw private transcript; it records the meaningful prompts, decisions, corrections, and verification steps used to produce the submitted repository.

## Main Prompt Themes

| Stage | User / AI Interaction | Result in Repository |
|---|---|---|
| Assignment interpretation | User provided Homework 02 requirements and asked for a full DQN stock-trading project. | `README.md`, `docs/PRD.md`, `docs/PLAN.md`, `docs/TODO.md`, mechanism PRDs. |
| Implementation plan | User approved a plan for Python, PyTorch, yfinance, Dueling DQN, Tkinter GUI, tests, and experiment evidence. | `src/dqn_trader/`, `config/`, `tests/`, `scripts/`, `assets/`, `results/experiments/`. |
| GitHub publishing | User asked to create a public GitHub repository named like the folder and push it. | Public repository and commit history were created. |
| GUI improvement | User said the initial GUI looked weak and asked for better styling, plots, and README screenshots. | Tkinter dashboard tabs, chart panels, style module, README visual assets. |
| Experiment evidence | User emphasized that the professor wanted to see experiments and hard work. | `docs/EXPERIMENTS.md`, `results/experiments/REPORT.md`, committed plots and metrics. |
| Backtest sanity check | User observed odd AAPL output with many trades and suspicious prediction. | Backtest now counts executed trades separately, masks impossible evaluation actions, and prediction uses the latest dataset window. |
| Training plot issue | User showed a misleading training chart. | Training now records `episode_losses`; GUI uses a dual-axis reward/loss chart. |
| Price correctness | User asked whether pulled prices are true. | Data client now calls `yfinance.download(..., auto_adjust=False)` and tests assert this behavior. README documents old adjusted-cache risk. |
| One-click workflow | User asked for one click to pull price, train, and backtest together. | `TradingSDK.run_pipeline()` and GUI `Run Full Pipeline` button. |
| Assessment feedback | User asked about cost awareness, chats, progress, commits, and source control. | This file, `docs/SOURCE_CONTROL.md`, `docs/ASSESSMENT_COVERAGE.md`, and expanded workflow/cost docs. |

## Important Corrections Made After Review

- The first backtest trade count was misleading because it counted action suggestions, not only executed trades.
- The first prediction implementation used the initial environment state; it now uses the latest available 30-day state window.
- The training chart originally mixed per-episode rewards with per-gradient-update losses; it now plots per-episode mean loss.
- The old AAPL parquet cache contained adjusted OHLC prices. The data client now requests raw split-adjusted Yahoo-style OHLCV with `auto_adjust=False` and a new `_raw.parquet` cache filename.
- The SPY comparison run failed because of a local yfinance/curl TLS certificate problem. The failure is documented instead of hidden.

## Verification Commands Used

```powershell
uv run ruff check
uv run ruff format --check
uv run pytest --cov=src --cov-report=term-missing
```

Latest recorded result: 24 tests passed with 96.60% coverage.

