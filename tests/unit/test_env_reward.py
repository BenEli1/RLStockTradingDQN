from dqn_trader.data.features import FeatureEngineer
from dqn_trader.env.reward import RewardFunction
from dqn_trader.env.trading_env import TradingEnv
from dqn_trader.shared.constants import Action


def make_env(raw_frame):
    features = FeatureEngineer().transform(raw_frame)
    return TradingEnv(features, raw_frame.loc[features.index, "Close"], 30, RewardFunction())


def test_reward_penalizes_costs():
    reward = RewardFunction(transaction_cost_alpha=0.01, slippage_beta=0.01)
    assert reward.compute(100, 101, traded=True, volatility=0) < reward.compute(100, 101, False, 0)


def test_env_reset_and_invalid_sell(raw_frame):
    env = make_env(raw_frame)
    state = env.reset()
    _next_state, reward, done, info = env.step(Action.SELL)
    assert state.shape == (30, 10)
    assert reward < 0
    assert not done
    assert info["portfolio_value"] > 0
