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
        self.geometry("1280x760")
        self.minsize(1120, 680)
        self.sdk = TradingSDK()
        self.ticker = tk.StringVar(value=self.sdk.config["data"]["ticker"])
        self.episodes = tk.StringVar(value=str(self.sdk.config["training"]["episodes"]))
        self.status = tk.StringVar(value="Ready")
        self.summary = tk.StringVar(value="No run yet")
        self.prediction = tk.StringVar(value="No prediction yet")
        self._build()

    def _build(self) -> None:
        apply_dashboard_style(self)
        shell = ttk.Frame(self, padding=8)
        shell.pack(fill="both", expand=True)
        shell.columnconfigure(1, weight=1)
        shell.columnconfigure(2, weight=0, minsize=260)
        shell.rowconfigure(0, weight=1)
        controls = ttk.LabelFrame(shell, text="Run Controls", padding=8)
        controls.grid(row=0, column=0, sticky="ns", padx=(0, 10))
        ttk.Label(controls, text="Ticker").pack(anchor="w")
        ttk.Entry(controls, textvariable=self.ticker, width=14).pack(fill="x", pady=(0, 8))
        ttk.Label(controls, text="Episodes").pack(anchor="w")
        ttk.Entry(controls, textvariable=self.episodes, width=14).pack(fill="x", pady=(0, 10))
        for label, command in [
            ("Prepare Data", self._prepare),
            ("Train", self._train),
            ("Backtest", self._backtest),
            ("Predict", self._predict),
        ]:
            ttk.Button(controls, text=label, command=command, style="Accent.TButton").pack(
                fill="x", pady=3
            )
        ttk.Button(
            controls,
            text="Run Full Pipeline",
            command=self._run_full_pipeline,
            style="Primary.TButton",
        ).pack(fill="x", pady=(9, 4))
        ttk.Separator(controls).pack(fill="x", pady=9)
        ttk.Label(controls, textvariable=self.summary, wraplength=170).pack(anchor="w")
        ttk.Separator(controls).pack(fill="x", pady=9)
        ttk.Label(controls, text="Prediction").pack(anchor="w")
        self.prediction_label = tk.Label(
            controls,
            textvariable=self.prediction,
            bg="#ffffff",
            fg="#6b7280",
            font=("Segoe UI", 18, "bold"),
            relief="solid",
            bd=1,
            padx=8,
            pady=8,
        )
        self.prediction_label.pack(fill="x", pady=(4, 0))
        dashboard = ttk.Frame(shell, padding=2)
        dashboard.grid(row=0, column=1, sticky="nsew")
        dashboard.columnconfigure(0, weight=1)
        dashboard.columnconfigure(1, weight=1)
        dashboard.rowconfigure(0, weight=2)
        dashboard.rowconfigure(1, weight=3)
        self.data_chart = self._dashboard_chart(dashboard, "Market Data", 0, 0)
        self.training_chart = self._dashboard_chart(dashboard, "Training", 0, 1)
        self.backtest_chart = self._dashboard_chart(dashboard, "Backtest", 1, 0, columnspan=2)
        self.data_chart.draw_empty("Prepare data to show close prices")
        self.training_chart.draw_empty("Train to show reward and mean loss")
        self.backtest_chart.draw_empty("Backtest to show DQN vs Buy-and-Hold equity")
        log_panel = ttk.LabelFrame(shell, text="Run Log", padding=8)
        log_panel.grid(row=0, column=2, sticky="nsew", padx=(8, 0))
        log_panel.rowconfigure(0, weight=1)
        log_panel.columnconfigure(0, weight=1)
        self.log = tk.Text(log_panel, width=32, height=12, wrap="word")
        self.log.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(log_panel, orient="vertical", command=self.log.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log.configure(yscrollcommand=scrollbar.set)
        ttk.Label(shell, textvariable=self.status, style="Status.TLabel").grid(
            row=1, column=0, columnspan=3, sticky="ew", pady=(6, 0)
        )
        self._write_log(
            "Ready. Use Run Full Pipeline for the complete demo, or run each stage manually."
        )

    def _prepare(self) -> None:
        ticker = self.ticker.get()

        def task():
            self._progress("Preparing market data and features. Usually a few seconds if cached.")
            raw, features, splits = self.sdk.prepare_data(ticker)
            close_values = raw["Close"].tolist()
            split_sizes = [len(part) for part in splits]

            def update() -> None:
                self.data_chart.draw_lines({"Close": close_values}, "Close Price", "Price")
                self.summary.set(
                    f"Raw rows: {len(raw)}\nFeature rows: {len(features)}\n"
                    f"Split sizes: {split_sizes}"
                )

            return "Data prepared. Market chart and split summary updated.", update

        self._run(task)

    def _run_full_pipeline(self) -> None:
        ticker = self.ticker.get()
        episodes = int(self.episodes.get())

        def task():
            self._progress(
                f"Full pipeline started for {ticker.upper()}: data -> train -> backtest -> predict."
            )
            self.sdk.config["training"]["episodes"] = episodes
            result = self.sdk.run_pipeline(ticker, progress=self._progress)
            self._progress(f"Complete: finished training/backtest/prediction for {ticker.upper()}.")
            labels = ["SELL", "HOLD", "BUY"]
            action, q_values = result.prediction
            split_sizes = [len(part) for part in result.splits]
            first_date = result.raw.index.min().date()
            last_date = result.raw.index.max().date()
            first_close = float(result.raw["Close"].iloc[0])
            last_close = float(result.raw["Close"].iloc[-1])

            def update() -> None:
                self.data_chart.draw_lines(
                    {"Close": result.raw["Close"].tolist()}, "Close Price", "Price"
                )
                self.training_chart.draw_dual_axis(
                    {"Reward": result.training.rewards},
                    {"Mean loss": result.training.episode_losses},
                    "Training Reward and Mean Loss",
                    "Episode reward",
                    "Mean loss",
                )
                self.backtest_chart.draw_lines(
                    {
                        "DQN": result.backtest.equity_curve,
                        "Buy-and-Hold": result.backtest.buy_hold_curve,
                    },
                    "Backtest Equity Curve",
                    "Portfolio Value",
                )
                self.summary.set(
                    f"{ticker.upper()} {first_date} -> {last_date}\n"
                    f"Close: {first_close:.2f} -> {last_close:.2f}\n"
                    f"Feature rows: {len(result.features)}\nSplit sizes: {split_sizes}\n"
                    f"Prediction: {labels[action]}"
                )
                self._set_prediction(labels[action])

            message = (
                f"Full pipeline completed: {ticker.upper()} close={first_close:.2f}->{last_close:.2f}, "
                f"return={result.backtest.total_return:.3f}, "
                f"buy_hold={result.backtest.buy_hold_return:.3f}, "
                f"executed_trades={result.backtest.trade_count}, prediction={labels[action]}, "
                f"q_values={[round(value, 4) for value in q_values]}"
            )
            return message, update

        self._run(task)

    def _train(self) -> None:
        ticker = self.ticker.get()
        episodes = int(self.episodes.get())

        def task():
            self._progress(
                f"Training {ticker.upper()} for {episodes} episodes. "
                "On CPU this can take roughly 10-60 seconds for the default setup."
            )
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
            self._progress("Running deterministic backtest. Usually a few seconds after training.")
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
            self._progress(
                "Predicting latest available dataset state. This is not a 2026-live pull."
            )
            action, q_values = self.sdk.predict_latest(ticker)
            labels = ["SELL", "HOLD", "BUY"]
            ordered = sorted(q_values, reverse=True)
            margin = ordered[0] - ordered[1] if len(ordered) > 1 else 0.0
            confidence = "low" if margin < 0.05 else "medium" if margin < 0.15 else "high"
            label = labels[action]

            def update() -> None:
                self._set_prediction(label)

            return (
                f"Prediction: {labels[action]} | confidence={confidence} | "
                f"margin={margin:.4f} | Q-values={q_values}"
            ), update

        self._run(task)

    def _run(self, func) -> None:
        def worker() -> None:
            try:
                message, update = func()
                self.after(0, self._finish_run, message, update)
            except Exception as exc:
                self.after(0, self._finish_run, f"Error: {exc}", None)

        threading.Thread(target=worker, daemon=True).start()

    def _progress(self, message: str) -> None:
        self.after(0, self.status.set, message)
        self.after(0, self._write_log, message)

    def _finish_run(self, message: str, update) -> None:
        if update is not None:
            update()
        self.status.set(message)
        self._write_log(message)

    def _dashboard_chart(
        self, parent: ttk.Frame, label: str, row: int, column: int, columnspan: int = 1
    ) -> ChartPanel:
        frame = ttk.LabelFrame(parent, text=label, padding=8)
        frame.grid(row=row, column=column, columnspan=columnspan, sticky="nsew", padx=4, pady=4)
        chart = ChartPanel(frame, label)
        return chart

    def _set_prediction(self, label: str) -> None:
        colors = {
            "BUY": ("#dcfce7", "#166534"),
            "HOLD": ("#f3f4f6", "#374151"),
            "SELL": ("#fee2e2", "#991b1b"),
        }
        background, foreground = colors.get(label, ("#ffffff", "#6b7280"))
        self.prediction.set(label)
        self.prediction_label.configure(bg=background, fg=foreground)

    def _write_log(self, text: str) -> None:
        self.log.insert("end", f"{text}\n")
        self.log.see("end")


def launch_gui() -> None:
    TraderApp().mainloop()
