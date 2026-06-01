"""Command-line entry point."""

import argparse

from dqn_trader.interface.gui import launch_gui
from dqn_trader.sdk.sdk import TradingSDK


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["prepare", "train", "backtest", "predict", "gui"])
    parser.add_argument("--ticker", default=None)
    args = parser.parse_args()
    sdk = TradingSDK()
    if args.command == "prepare":
        raw, features, _splits = sdk.prepare_data(args.ticker)
        print(f"raw_rows={len(raw)} feature_rows={len(features)}")
        print(raw.head().to_string())
        print(features.head().to_string())
    elif args.command == "train":
        result = sdk.train(args.ticker)
        print(f"episodes={len(result.rewards)} checkpoint={result.checkpoint_path}")
    elif args.command == "backtest":
        result = sdk.backtest(args.ticker)
        print(
            f"return={result.total_return:.4f} drawdown={result.max_drawdown:.4f} "
            f"executed_trades={result.trade_count} invalid_actions={result.invalid_action_count}"
        )
    elif args.command == "predict":
        action, q_values = sdk.predict_latest(args.ticker)
        ordered = sorted(q_values, reverse=True)
        margin = ordered[0] - ordered[1] if len(ordered) > 1 else 0.0
        confidence = "low" if margin < 0.05 else "medium" if margin < 0.15 else "high"
        print(f"action={action} confidence={confidence} margin={margin:.4f} q_values={q_values}")
    else:
        launch_gui()


if __name__ == "__main__":
    main()
