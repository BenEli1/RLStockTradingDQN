# Source Control and Progress Evidence

The project was managed through Git and pushed to a public GitHub repository:

<https://github.com/BenEli1/RLStockTradingDQN>

The repository history shows iterative development instead of a single final dump.

## Commit Timeline

| Commit | Purpose |
|---|---|
| `bea1723` | Built the initial DQN trader assignment project structure and implementation. |
| `0599b63` | Audited and hardened the submission against assignment requirements. |
| `84caebc` | Improved the GUI dashboard and added a code-connected RL tutorial. |
| `5d76d31` | Added README visual demonstration assets. |
| `e5dabc8` | Aligned real GUI styling with README preview images. |
| `206dd19` | Added experiment evidence and a submission-focused README. |
| `fd88fcf` | Fixed latest prediction behavior and executable backtest policy. |
| `799e0b4` | Fixed misleading training chart scaling. |
| `7de9d21` | Added one-click GUI pipeline and raw-price validation tests. |

## Source-Control Practices Used

- Meaningful commits were created after functional milestones.
- Generated caches, virtual environments, Python caches, and large checkpoints are ignored.
- Results that support the report, such as experiment metrics and plots, are committed when they are small enough to be useful evidence.
- The worktree was checked before committing to avoid staging unrelated files.
- The final branch is `main`, tracking `origin/main`.

## Current Quality Gate

The latest pushed state was validated with:

```powershell
uv run ruff check
uv run ruff format --check
uv run pytest --cov=src --cov-report=term-missing
```

Latest recorded result: 25 tests passed with 96.07% coverage.
