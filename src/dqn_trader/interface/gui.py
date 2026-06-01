"""Tkinter GUI that delegates all business logic to the SDK."""

import threading
import tkinter as tk
from tkinter import ttk

from dqn_trader.interface.charts import ChartPanel
from dqn_trader.interface.style import apply_dashboard_style
from dqn_trader.sdk.sdk import TradingSDK


class TraderApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("DQN Trader SDK - Assignment 02")
        self.geometry("1120x720")
        self.minsize(980, 640)
        self.sdk = TradingSDK()
        self.ticker = tk.StringVar(value=self.sdk.config["data"]["ticker"])
        self.episodes = tk.StringVar(value=str(self.sdk.config["training"]["episodes"]))
        self.status = tk.StringVar(value="Ready")
        self.summary = tk.StringVar(value="No run yet")
        self._build()

    def _build(self) -> None:
        apply_dashboard_style(self)
        header = tk.Frame(self, bg="#1f2937", height=72)
        header.pack(fill="x")
        tk.Label(
            header,
            text="DQN Trader SDK - Tkinter Dashboard",
            bg="#1f2937",
            fg="#ffffff",
            font=("Segoe UI", 20, "bold"),
            padx=24,
            pady=18,
        ).pack(anchor="w")
        shell = ttk.Frame(self, padding=16)
        shell.pack(fill="both", expand=True)
        shell.columnconfigure(1, weight=1)
        shell.rowconfigure(1, weight=1)
        controls = ttk.LabelFrame(shell, text="Run Controls", padding=12)
        controls.grid(row=0, column=0, sticky="ns", padx=(0, 14))
        ttk.Label(controls, text="Ticker").pack(anchor="w")
        ttk.Entry(controls, textvariable=self.ticker, width=16).pack(fill="x", pady=(0, 10))
        ttk.Label(controls, text="Episodes").pack(anchor="w")
        ttk.Entry(controls, textvariable=self.episodes, width=16).pack(fill="x", pady=(0, 14))
        for label, command in [
            ("Prepare Data", self._prepare),
            ("Train", self._train),
            ("Backtest", self._backtest),
            ("Predict", self._predict),
        ]:
            ttk.Button(controls, text=label, command=command, style="Accent.TButton").pack(
                fill="x", pady=4
            )
        ttk.Separator(controls).pack(fill="x", pady=12)
        ttk.Label(controls, textvariable=self.summary, wraplength=190).pack(anchor="w")
        self.tabs = ttk.Notebook(shell)
        self.tabs.grid(row=0, column=1, sticky="nsew")
        self.data_chart = self._tab("Market Data", "Close price")
        self.training_chart = self._tab("Training", "Episode reward / loss")
        self.backtest_chart = self._tab("Backtest", "Equity curve")
        self.log = tk.Text(self.tabs, height=8, wrap="word")
        self.tabs.add(self.log, text="Run Log")
        ttk.Label(shell, textvariable=self.status, style="Status.TLabel").grid(
            row=1, column=0, columnspan=2, sticky="ew", pady=(12, 0)
        )
        self._write_log("Ready. Use Prepare Data first, then Train and Backtest.")

    def _prepare(self) -> None:
        ticker = self.ticker.get()

        def task():
            raw, features, splits = self.sdk.prepare_data(ticker)
            close_values = raw["Close"].tolist()
            split_sizes = [len(part) for part in splits]

            def update() -> None:
                self.data_chart.draw_lines({"Close": close_values}, "Close Price", "Price")
                self.summary.set(
                    f"Raw rows: {len(raw)}\nFeature rows: {len(features)}\n"
                    f"Split sizes: {split_sizes}"
                )

            return "Data prepared", update

        self._run(task)

    def _train(self) -> None:
        ticker = self.ticker.get()
        episodes = int(self.episodes.get())

        def task():
            self.sdk.config["training"]["episodes"] = episodes
            result = self.sdk.train(ticker)

            def update() -> None:
                self.training_chart.draw_dual_axis(
                    {"Reward": result.rewards},
                    {"Mean loss": result.episode_losses},
                    "Training Reward and Mean Loss",
                    "Episode reward",
                    "Mean loss",
                )

            return f"Training completed. Checkpoint: {result.checkpoint_path}", update

        self._run(task)

    def _backtest(self) -> None:
        ticker = self.ticker.get()

        def task():
            result = self.sdk.backtest(ticker)

            def update() -> None:
                self.backtest_chart.draw_lines(
                    {"DQN": result.equity_curve, "Buy-and-Hold": result.buy_hold_curve},
                    "Backtest Equity Curve",
                    "Portfolio Value",
                )

            message = (
                f"Backtest: return={result.total_return:.3f}, "
                f"buy_hold={result.buy_hold_return:.3f}, sharpe={result.sharpe_ratio:.3f}, "
                f"drawdown={result.max_drawdown:.3f}, executed_trades={result.trade_count}, "
                f"invalid_actions={result.invalid_action_count}"
            )
            return message, update

        self._run(task)

    def _predict(self) -> None:
        ticker = self.ticker.get()

        def task():
            action, q_values = self.sdk.predict_latest(ticker)
            labels = ["SELL", "HOLD", "BUY"]
            ordered = sorted(q_values, reverse=True)
            margin = ordered[0] - ordered[1] if len(ordered) > 1 else 0.0
            confidence = "low" if margin < 0.05 else "medium" if margin < 0.15 else "high"
            return (
                f"Prediction: {labels[action]} | confidence={confidence} | "
                f"margin={margin:.4f} | Q-values={q_values}"
            ), None

        self._run(task)

    def _run(self, func) -> None:
        def worker() -> None:
            try:
                self.after(0, self.status.set, "Running...")
                message, update = func()
                self.after(0, self._finish_run, message, update)
            except Exception as exc:
                self.after(0, self._finish_run, f"Error: {exc}", None)

        threading.Thread(target=worker, daemon=True).start()

    def _finish_run(self, message: str, update) -> None:
        if update is not None:
            update()
        self.status.set(message)
        self._write_log(message)

    def _tab(self, label: str, empty_message: str) -> ChartPanel:
        frame = ttk.Frame(self.tabs, padding=10)
        self.tabs.add(frame, text=label)
        chart = ChartPanel(frame, label)
        chart.draw_empty(empty_message)
        return chart

    def _write_log(self, text: str) -> None:
        self.log.insert("end", f"{text}\n")
        self.log.see("end")


def launch_gui() -> None:
    TraderApp().mainloop()
