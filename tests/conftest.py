from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture
def raw_frame() -> pd.DataFrame:
    dates = pd.date_range("2020-01-01", periods=90, freq="D")
    close = pd.Series(range(100, 190), index=dates, dtype=float)
    return pd.DataFrame(
        {
            "Open": close - 1,
            "High": close + 2,
            "Low": close - 2,
            "Close": close,
            "Volume": [1000 + i for i in range(90)],
        },
        index=dates,
    )


@pytest.fixture
def config_file(tmp_path: Path) -> Path:
    path = tmp_path / "setup.yaml"
    path.write_text('version: "1.00"\nsection:\n  value: 3\n', encoding="utf-8")
    return path
