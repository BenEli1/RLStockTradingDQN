import pandas as pd

from dqn_trader.data.client import YFinanceDataClient


def test_client_uses_csv_fallback_when_download_fails(monkeypatch, tmp_path, raw_frame):
    def fail_download(*_args, **_kwargs):
        raise RuntimeError("offline")

    monkeypatch.setattr("dqn_trader.data.client.yf.download", fail_download)
    raw_frame.to_csv(tmp_path / "AAPL.csv", index_label="Date")
    loaded = YFinanceDataClient(tmp_path).load_daily("AAPL", "2020-01-01", "2023-01-01")
    pd.testing.assert_frame_equal(loaded, raw_frame, check_freq=False)


def test_client_ignores_corrupt_cache_and_downloads(monkeypatch, tmp_path, raw_frame):
    (tmp_path / "AAPL_2020-01-01_2023-01-01.parquet").write_text("bad cache", encoding="utf-8")
    monkeypatch.setattr("dqn_trader.data.client.yf.download", lambda *_args, **_kwargs: raw_frame)
    loaded = YFinanceDataClient(tmp_path).load_daily("AAPL", "2020-01-01", "2023-01-01")
    pd.testing.assert_frame_equal(loaded, raw_frame)
