from dqn_trader.data.features import FeatureEngineer


def test_features_and_windows_have_required_shape(raw_frame):
    engineer = FeatureEngineer(window_size=30)
    features = engineer.transform(raw_frame)
    windows = engineer.make_windows(features)
    assert list(features.columns) == [
        "log_return",
        "rsi_14",
        "macd",
        "macd_signal",
        "macd_hist",
        "bb_pct",
        "vwap_dist",
        "volume_norm",
        "position",
        "unrealised_pnl",
    ]
    assert windows.shape[1:] == (30, 10)


def test_chronological_split_keeps_order(raw_frame):
    train, validation, test = FeatureEngineer.chronological_split(raw_frame, 0.7, 0.15)
    assert train.index.max() < validation.index.min()
    assert validation.index.max() < test.index.min()
