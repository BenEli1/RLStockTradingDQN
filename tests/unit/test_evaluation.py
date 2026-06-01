from dqn_trader.data.features import FeatureEngineer
from dqn_trader.env.reward import RewardFunction
from dqn_trader.env.trading_env import TradingEnv
from dqn_trader.evaluation.backtest import BacktestService, InferenceService
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
    assert -1 <= result.max_drawdown <= 0
