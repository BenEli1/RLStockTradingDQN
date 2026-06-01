from dqn_trader.data.features import FeatureEngineer
from dqn_trader.sdk.sdk import TradingSDK


def test_sdk_make_env_basic_reward(monkeypatch, raw_frame):
    monkeypatch.setattr(
        "dqn_trader.data.client.YFinanceDataClient.load_daily",
        lambda *_args, **_kwargs: raw_frame,
    )
    sdk = TradingSDK()
    raw, features, _splits = sdk.prepare_data("AAPL")
    env = sdk.make_env(features, raw, reward_mode="basic")
    assert env.reset().shape == (30, 10)


def test_make_windows_rejects_short_frame(raw_frame):
    features = FeatureEngineer(window_size=30).transform(raw_frame).head(3)
    try:
        FeatureEngineer(window_size=30).make_windows(features)
    except ValueError as exc:
        assert "Not enough rows" in str(exc)
