"""Yahoo Finance data client with parquet cache and CSV fallback."""

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import yfinance as yf

from dqn_trader.shared.constants import RAW_COLUMNS


@dataclass
class YFinanceDataClient:
    cache_dir: Path

    def load_daily(self, ticker: str, start: str, end: str, interval: str = "1d") -> pd.DataFrame:
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file = self.cache_dir / f"{ticker}_{start}_{end}.parquet"
        csv_fallback = self.cache_dir / f"{ticker}.csv"
        if cache_file.exists():
            try:
                return self._select(pd.read_parquet(cache_file))
            except Exception:
                # A partial/corrupt cache should not block the required data path.
                pass
        try:
            frame = yf.download(ticker, start=start, end=end, interval=interval, progress=False)
            if isinstance(frame.columns, pd.MultiIndex):
                frame.columns = frame.columns.droplevel(1)
            if frame.empty:
                raise ValueError(f"No data returned for {ticker}")
            frame = self._select(frame)
            frame.to_parquet(cache_file, compression="snappy")
            return frame
        except Exception:
            if not csv_fallback.exists():
                raise
            return self._select(pd.read_csv(csv_fallback, index_col="Date", parse_dates=True))

    @staticmethod
    def _select(frame: pd.DataFrame) -> pd.DataFrame:
        missing = [column for column in RAW_COLUMNS if column not in frame.columns]
        if missing:
            raise ValueError(f"Missing OHLCV columns: {missing}")
        selected = frame[RAW_COLUMNS].copy()
        selected.index = pd.to_datetime(selected.index)
        selected.index.name = None
        return selected.sort_index()
