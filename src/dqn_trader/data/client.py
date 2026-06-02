"""Yahoo Finance data client with parquet cache and CSV fallback."""

import json
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import yfinance as yf
import yfinance.cache as yf_cache

from dqn_trader.shared.constants import RAW_COLUMNS


@dataclass
class YFinanceDataClient:
    cache_dir: Path

    def load_daily(self, ticker: str, start: str, end: str, interval: str = "1d") -> pd.DataFrame:
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file = self.cache_dir / f"{ticker}_{start}_{end}_{interval}_raw.parquet"
        csv_fallback = self.cache_dir / f"{ticker}.csv"
        yf_cache.set_cache_location(str(self.cache_dir / ".yfinance-cache"))
        if cache_file.exists():
            try:
                return self._select(pd.read_parquet(cache_file))
            except Exception:
                # A partial/corrupt cache should not block the required data path.
                pass
        try:
            frame = yf.download(
                ticker,
                start=start,
                end=end,
                interval=interval,
                progress=False,
                auto_adjust=False,
            )
            if isinstance(frame.columns, pd.MultiIndex):
                frame.columns = frame.columns.droplevel(1)
            if frame.empty:
                raise ValueError(f"No data returned for {ticker}")
            frame = self._select(frame)
            frame.to_parquet(cache_file, compression="snappy")
            return frame
        except Exception:
            try:
                frame = self._download_yahoo_chart(ticker, start, end, interval)
                frame.to_parquet(cache_file, compression="snappy")
                return frame
            except Exception:
                pass
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

    @classmethod
    def _download_yahoo_chart(
        cls, ticker: str, start: str, end: str, interval: str
    ) -> pd.DataFrame:
        start_ts = int(pd.Timestamp(start, tz="UTC").timestamp())
        end_ts = int(pd.Timestamp(end, tz="UTC").timestamp())
        params = urllib.parse.urlencode(
            {
                "period1": start_ts,
                "period2": end_ts,
                "interval": interval,
                "events": "history",
            }
        )
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?{params}"
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read())
        result = payload["chart"]["result"][0]
        quote = result["indicators"]["quote"][0]
        frame = pd.DataFrame(
            {
                "Open": quote["open"],
                "High": quote["high"],
                "Low": quote["low"],
                "Close": quote["close"],
                "Volume": quote["volume"],
            },
            index=pd.to_datetime(result["timestamp"], unit="s"),
        ).dropna()
        if frame.empty:
            raise ValueError(f"No data returned for {ticker}")
        return cls._select(frame)
