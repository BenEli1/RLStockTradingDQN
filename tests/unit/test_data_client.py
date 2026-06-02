import pandas as pd
import pytest

from dqn_trader.data.client import YFinanceDataClient


def test_client_downloads_raw_prices_with_explicit_adjustment(monkeypatch, tmp_path, raw_frame):
    captured = {}

    def download(*_args, **kwargs):
        captured.update(kwargs)
        return raw_frame

    monkeypatch.setattr("dqn_trader.data.client.yf.download", download)
    loaded = YFinanceDataClient(tmp_path).load_daily("AAPL", "2020-01-01", "2023-01-01")
    assert captured["auto_adjust"] is False
    assert captured["progress"] is False
    assert (tmp_path / "AAPL_2020-01-01_2023-01-01_1d_raw.parquet").exists()
    pd.testing.assert_frame_equal(loaded, raw_frame)


def test_client_uses_csv_fallback_when_download_fails(monkeypatch, tmp_path, raw_frame):
    def fail_download(*_args, **_kwargs):
        raise RuntimeError("offline")

    monkeypatch.setattr("dqn_trader.data.client.yf.download", fail_download)
    raw_frame.to_csv(tmp_path / "AAPL.csv", index_label="Date")
    loaded = YFinanceDataClient(tmp_path).load_daily("AAPL", "2020-01-01", "2023-01-01")
    pd.testing.assert_frame_equal(loaded, raw_frame, check_freq=False)


def test_client_ignores_corrupt_cache_and_downloads(monkeypatch, tmp_path, raw_frame):
    (tmp_path / "AAPL_2020-01-01_2023-01-01_1d_raw.parquet").write_text(
        "bad cache", encoding="utf-8"
    )
    monkeypatch.setattr("dqn_trader.data.client.yf.download", lambda *_args, **_kwargs: raw_frame)
    loaded = YFinanceDataClient(tmp_path).load_daily("AAPL", "2020-01-01", "2023-01-01")
    pd.testing.assert_frame_equal(loaded, raw_frame)


def test_client_flattens_yfinance_multiindex(monkeypatch, tmp_path, raw_frame):
    multi = raw_frame.copy()
    multi.columns = pd.MultiIndex.from_product([multi.columns, ["AAPL"]])
    monkeypatch.setattr("dqn_trader.data.client.yf.download", lambda *_args, **_kwargs: multi)
    loaded = YFinanceDataClient(tmp_path).load_daily("AAPL", "2020-01-01", "2023-01-01")
    pd.testing.assert_frame_equal(loaded, raw_frame)


def test_client_raises_when_download_and_fallback_fail(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "dqn_trader.data.client.yf.download",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(ValueError("network")),
    )
    with pytest.raises(ValueError, match="network"):
        YFinanceDataClient(tmp_path).load_daily("AAPL", "2020-01-01", "2023-01-01")
