from pathlib import Path

from dqn_trader.data.features import FeatureEngineer
from dqn_trader.env.reward import RewardFunction
from dqn_trader.env.trading_env import TradingEnv
from dqn_trader.sdk.sdk import TradingSDK
from dqn_trader.training.service import TrainingService


def test_training_writes_checkpoint(tmp_path, raw_frame):
    features = FeatureEngineer().transform(raw_frame)
    env = TradingEnv(features, raw_frame.loc[features.index, "Close"], 30, RewardFunction())
    config = {
        "episodes": 1,
        "batch_size": 4,
        "gamma": 0.99,
        "learning_rate": 0.001,
        "epsilon_start": 0.1,
        "epsilon_end": 0.05,
        "epsilon_decay": 0.9,
        "replay_capacity": 100,
        "target_update_steps": 50,
    }
    result = TrainingService(config).train(env, tmp_path / "model.pt")
    assert Path(result.checkpoint_path).exists()


def test_sdk_prepare_data_uses_client(monkeypatch, raw_frame):
    monkeypatch.setattr(
        "dqn_trader.data.client.YFinanceDataClient.load_daily",
        lambda *_args, **_kwargs: raw_frame,
    )
    raw, features, splits = TradingSDK().prepare_data("AAPL")
    assert len(raw) == len(raw_frame)
    assert len(features) > 0
    assert len(splits) == 3
