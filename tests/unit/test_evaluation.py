from dqn_trader.data.features import FeatureEngineer
from dqn_trader.env.reward import RewardFunction
from dqn_trader.env.trading_env import TradingEnv
from dqn_trader.evaluation.backtest import BacktestResult, BacktestService, InferenceService
from dqn_trader.model.network import DuelingDQNNetwork


def test_inference_and_backtest(raw_frame):
    features = FeatureEngineer().transform(raw_frame)
    env = TradingEnv(features, raw_frame.loc[features.index, "Close"], 30, RewardFunction())
    model = DuelingDQNNetwork(30, 10)
    action, q_values = InferenceService.predict(model, env.reset())
    result = BacktestService().run(env, model)
    assert action in {0, 1, 2}
    assert len(q_values) == 3
    assert result.equity_curve
    assert result.buy_hold_curve
    assert isinstance(result.sharpe_ratio, float)
    assert result.trade_count >= 0
    assert result.invalid_action_count >= 0
    assert len(result.executed_trades) == len(result.actions)
    assert -1 <= result.max_drawdown <= 0


def test_inference_masks_illegal_actions(raw_frame):
    features = FeatureEngineer().transform(raw_frame)
    model = DuelingDQNNetwork(30, 10)
    state = features.tail(30).to_numpy(dtype="float32")
    no_position_action, no_position_q = InferenceService.predict(model, state, has_position=False)
    has_position_action, has_position_q = InferenceService.predict(model, state, has_position=True)
    assert no_position_action != 0
    assert has_position_action != 2
    assert len(no_position_q) == 3
    assert len(has_position_q) == 3


def test_backtest_save_writes_metrics_and_plot(tmp_path):
    result = BacktestResult(
        equity_curve=[10000.0, 10100.0, 9900.0],
        buy_hold_curve=[10000.0, 10050.0, 10100.0],
        actions=[1, 2, 0],
        executed_trades=[0, 1, 1],
        total_return=-0.01,
        buy_hold_return=0.01,
        sharpe_ratio=0.5,
        max_drawdown=-0.02,
        win_rate=0.4,
        trade_count=2,
        invalid_action_count=0,
    )
    BacktestService.save(result, tmp_path)
    assert (tmp_path / "backtest_metrics.json").exists()
    assert (tmp_path / "backtest_equity.png").exists()
