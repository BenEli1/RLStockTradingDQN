# RL Tutorial: How This Project Makes Trading Decisions

## How Reinforcement Learning Makes Trading Decisions
This project is a Reinforcement Learning / DQN educational system. It is not a stock price prediction model and it is not financial advice. The agent learns a policy: given the current market and portfolio state, choose `Sell`, `Hold`, or `Buy` to maximize expected long-term return.

| RL concept | Code module | Meaning in this project |
|---|---|---|
| Agent | `dqn_trader.model.network.DuelingDQNNetwork` | Policy network that estimates action values |
| Environment | `dqn_trader.env.trading_env.TradingEnv` | Market and portfolio simulator |
| State | `FeatureEngineer` + `TradingEnv._state()` | Historical 30-day market window plus portfolio channels |
| Action | `dqn_trader.shared.constants.Action` | `SELL=0`, `HOLD=1`, `BUY=2` |
| Reward | `dqn_trader.env.reward.RewardFunction` | Portfolio return minus costs and risk penalty |
| Episode | `TrainingService.train()` | One chronological pass over historical data |
| Policy | `InferenceService.predict()` | Choose the action with highest Q-value during evaluation |
| Return | `TrainingService._learn()` | Immediate reward plus discounted future value |

## From Q-Table to DQN
In a tiny toy problem, we could store `Q(state, action)` in a table. Real market data is different: a state is not just "price up" or "price down"; it is a continuous window of many numeric features. This makes a Q-table impossible to maintain.

| Aspect | Q-table | DQN |
|---|---|---|
| Input | Discrete state ID | Feature tensor |
| Storage | Explicit table | Neural network weights |
| Output | Action score from a cell | Predicted Q-values |
| Works for | Tiny finite problems | Large continuous state spaces |
| Problem/benefit | Impossible for market windows | Generalizes to unseen windows |

`DuelingDQNNetwork` receives a `(30, 10)` state tensor and outputs three values: `Q(s, Sell)`, `Q(s, Hold)`, and `Q(s, Buy)`.

## From Raw Market Data to State Tensor
The data flow is implemented in `YFinanceDataClient` and `FeatureEngineer`.

1. Download daily OHLCV data from Yahoo Finance through `yfinance`.
2. Require raw columns: `Open`, `High`, `Low`, `Close`, `Volume`.
3. Cache parquet files under `data/raw/` and fall back to CSV if download fails.
4. Compute `log_return`, `rsi_14`, `macd`, `macd_signal`, `macd_hist`, `bb_pct`, `vwap_dist`, `volume_norm`, `position`, and `unrealised_pnl`.
5. Sort chronologically and split train/validation/test without shuffling.
6. Build sliding windows of 30 days, producing states shaped `(30, 10)`.

A single price point loses trend, volatility, momentum, and context. A 30-day window lets the model observe short historical patterns before choosing an action.

## How the Network Chooses Buy, Sell, or Hold
1. `TradingEnv` creates the current 30 by 10 state window.
2. The state tensor is passed into `DuelingDQNNetwork`.
3. The compact MLP flattens the window and learns feature interactions across the historical context.
4. The value stream estimates how good the current state is.
5. The advantage stream estimates how much better each action is than the others.
6. The output is combined as `Q(s,a) = V(s) + (A(s,a) - mean_a A(s,a))`.
7. During training, `TrainingService` uses epsilon-greedy exploration.
8. During backtesting, `InferenceService` chooses `argmax Q(s,a)` without random exploration.
9. The selected action is passed to `env.step(action)`.
10. The environment updates cash, position, portfolio value, reward, and next state.

Dueling DQN is useful here because `Hold` is often reasonable and the differences between active actions can be subtle.

## Reward Function
`RewardFunction.compute()` encourages portfolio growth while subtracting costs and risk:

```text
reward = portfolio_return - transaction_cost - slippage - risk_penalty - invalid_action_penalty
```

The invalid-action penalty is applied by `TradingEnv.step()` for impossible active actions such as selling without a position or buying while already holding. Reward based only on immediate profit is dangerous because the agent may overtrade, ignore fees, learn high-risk behavior, exploit environment bugs, or produce a nice-looking but unreliable backtest.

## Learning from Sequential Market Experiences
Every environment step produces a transition:

```text
(s, a, r, s_next, done)
```

`ReplayBuffer` stores these experiences and samples batches for learning. `TrainingService._learn()` computes the Bellman target:

```text
target = reward + gamma * max_a' Q_target(next_state, a') * (1 - done)
```

The policy network learns every optimizer step. The target network is copied from the policy network periodically to keep targets more stable.

## Backtesting and Trading Performance
`BacktestService` evaluates the trained model with greedy actions. Backtesting is a historical diagnostic, not proof of future profitability.

Metrics written to `results/backtest_metrics.json`:

- Total Return: final portfolio value compared to initial capital.
- Buy-and-Hold baseline: passive benchmark on the same price series.
- Sharpe Ratio: return relative to volatility.
- Max Drawdown: worst fall from peak to trough.
- Win Rate: percentage of positive-reward steps.
- Number of Trades: non-hold actions, useful for spotting overtrading.

Total return alone is not enough. A strategy can show high return while suffering unacceptable drawdown or unstable volatility. Sharpe helps judge whether profit was stable relative to risk, but it should not be the only objective.

## Setup and Execution Tutorial
Install dependencies:

```powershell
uv sync --extra dev
```

Prepare data:

```powershell
uv run dqn-trader prepare --ticker AAPL
```

Train:

```powershell
uv run dqn-trader train --ticker AAPL
```

Backtest:

```powershell
uv run dqn-trader backtest --ticker AAPL
```

Predict or launch GUI:

```powershell
uv run dqn-trader predict --ticker AAPL
uv run dqn-trader gui
```

Quality checks:

```powershell
uv run pytest --cov=src --cov-report=term-missing
uv run ruff check
uv run ruff format --check
```
