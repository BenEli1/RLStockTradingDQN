# TODO

| Status | Priority | Task | Definition of Done |
|---|---:|---|---|
| Done | High | Create repo structure | Required folders and config files exist |
| Done | High | Implement SDK facade | GUI/CLI can call business flows through SDK |
| Done | High | Implement data pipeline | yfinance cache and CSV fallback are covered by tests |
| Done | High | Implement feature engineering | Ten required features and windows are produced |
| Done | High | Implement trading environment | reset/step/actions/reward are tested |
| Done | High | Implement Dueling DQN | Forward pass returns three Q-values |
| Done | High | Implement replay and training | Training step saves checkpoint in integration test |
| Done | Medium | Implement Tkinter GUI | Prepare/train buttons call SDK only |
| Done | High | Write docs and diagrams | README and docs folder include required files |
| Done | High | Add audit improvement docs | AI workflow, cost analysis, version history, and experiment summary exist |
| Done | Medium | Add richer backtest metrics | Buy-and-Hold, Sharpe, drawdown, win rate, and trade count are reported |
| Done | Medium | Improve GUI presentation | GUI uses one dashboard with side log, status, prediction badge, and embedded charts |
| Done | Medium | Add RL tutorial | Code-connected tutorial explains Q-table, DQN, tensors, rewards, and backtesting |
| Done | Medium | Fix misleading training chart | Reward and per-episode mean loss are plotted on separate axes |
| Done | Medium | Add one-click GUI pipeline | One button prepares data, trains, backtests, predicts, and updates plots |
| Done | Medium | Validate raw price data path | Data client uses `auto_adjust=False` and tests enforce it |
| Done | Medium | Add source-control evidence | GitHub URL and commit timeline are documented |
| Done | Medium | Add AI chat/process evidence | AI-assisted workflow and chat summary are documented |
| Done | Medium | Add assessment coverage matrix | Requirements and feedback criteria are mapped to files |
| Done | Medium | Add screenshots/plots to README | Demo GUI assets and real experiment plots are referenced |
| Done | Medium | Add Yahoo Chart fallback | SPY and other symbols can run when yfinance/curl TLS fails locally |
| Done | Medium | Run broader multi-stock research | Ten compact diagnostic runs are documented under `results/multi_stock/` |
| Pending | Low | Run longer research experiments | Increase episodes and add repeated seeds after submission timing allows |
