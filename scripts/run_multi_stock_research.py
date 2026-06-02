"""Run the DQN pipeline on a broader ticker sample for research evidence."""

import csv
import json
from pathlib import Path
from typing import Any

from dqn_trader.sdk.sdk import TradingSDK

TICKERS = [
    ("AAPL", "Apple", "Technology"),
    ("NVDA", "NVIDIA", "Semiconductors / AI"),
    ("NFLX", "Netflix", "Streaming media"),
    ("META", "Meta Platforms", "Social media"),
    ("SPY", "S&P 500 ETF", "Market ETF"),
    ("AMZN", "Amazon", "E-commerce / cloud"),
    ("MCD", "McDonald's", "Consumer staples / restaurants"),
    ("KO", "Coca-Cola", "Consumer staples"),
    ("CRWD", "CrowdStrike", "Cybersecurity"),
    ("PFE", "Pfizer", "Healthcare / pharmaceuticals"),
]


def run_ticker(ticker: str, name: str, sector: str, episodes: int) -> dict[str, Any]:
    sdk = TradingSDK()
    output_dir = Path("results/multi_stock") / ticker.lower()
    sdk.config["training"]["episodes"] = episodes
    sdk.config["training"]["checkpoint_path"] = str(output_dir / "best_model.pt")
    result = sdk.run_pipeline(ticker, output_dir=output_dir)
    action, q_values = result.prediction
    labels = ["SELL", "HOLD", "BUY"]
    return {
        "ticker": ticker,
        "name": name,
        "sector": sector,
        "episodes": episodes,
        "status": "ok",
        "rows": len(result.raw),
        "feature_rows": len(result.features),
        "first_date": str(result.raw.index.min().date()),
        "last_date": str(result.raw.index.max().date()),
        "first_close": float(result.raw["Close"].iloc[0]),
        "last_close": float(result.raw["Close"].iloc[-1]),
        "final_training_reward": result.training.rewards[-1],
        "total_return": result.backtest.total_return,
        "buy_hold_return": result.backtest.buy_hold_return,
        "sharpe_ratio": result.backtest.sharpe_ratio,
        "max_drawdown": result.backtest.max_drawdown,
        "win_rate": result.backtest.win_rate,
        "trade_count": result.backtest.trade_count,
        "prediction": labels[action],
        "q_sell": q_values[0],
        "q_hold": q_values[1],
        "q_buy": q_values[2],
    }


def run_safely(ticker: str, name: str, sector: str, episodes: int) -> dict[str, Any]:
    try:
        return run_ticker(ticker, name, sector, episodes)
    except Exception as exc:
        return {
            "ticker": ticker,
            "name": name,
            "sector": sector,
            "episodes": episodes,
            "status": "failed",
            "error": str(exc),
        }


def write_outputs(rows: list[dict[str, Any]]) -> None:
    output_dir = Path("results/multi_stock")
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    fieldnames = sorted({key for row in rows for key in row})
    with (output_dir / "summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "REPORT.md").write_text(build_report(rows), encoding="utf-8")


def fmt(row: dict[str, Any], key: str) -> str:
    value = row.get(key)
    return "FAILED" if value is None else f"{float(value):.4f}"


def build_report(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Multi-Stock Research Report",
        "",
        "This report runs the same Dueling DQN pipeline across a broader set of well-known stocks and one ETF.",
        "The purpose is research coverage and robustness evidence, not financial advice or proof of future profitability.",
        "",
        "Command:",
        "",
        "```powershell",
        "uv run python scripts/run_multi_stock_research.py",
        "```",
        "",
        "Setup: daily Yahoo Finance/yfinance OHLCV, 2020-01-01 to 2023-01-01, chronological data, risk-adjusted reward, compact CPU-friendly training.",
        "",
        "| Ticker | Company / Asset | Sector | Status | DQN Return | Buy/Hold | Sharpe | Max Drawdown | Trades | Prediction |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        if row["status"] == "failed":
            lines.append(
                f"| {row['ticker']} | {row['name']} | {row['sector']} | failed | FAILED | FAILED | FAILED | FAILED | FAILED | FAILED |"
            )
            continue
        lines.append(
            f"| {row['ticker']} | {row['name']} | {row['sector']} | ok | "
            f"{fmt(row, 'total_return')} | {fmt(row, 'buy_hold_return')} | "
            f"{fmt(row, 'sharpe_ratio')} | {fmt(row, 'max_drawdown')} | "
            f"{row['trade_count']} | {row['prediction']} |"
        )
    failed = [row for row in rows if row["status"] == "failed"]
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This broad run checks whether the implementation can execute across different market regimes and sectors.",
            "- The model and episode count are intentionally compact for coursework timing, so the results should be read as engineering evidence rather than trading claims.",
            "- Buy-and-Hold remains the baseline because a DQN return is only meaningful when compared against a passive strategy on the same ticker and period.",
            "- Differences in trade count, drawdown, and Sharpe show that reward and market behavior interact differently across assets.",
        ]
    )
    if failed:
        lines.extend(["", "## Failed Runs", ""])
        for row in failed:
            lines.append(f"- `{row['ticker']}` failed with: `{row['error']}`")
    return "\n".join(lines) + "\n"


def main() -> None:
    rows = [run_safely(ticker, name, sector, episodes=3) for ticker, name, sector in TICKERS]
    write_outputs(rows)


if __name__ == "__main__":
    main()
