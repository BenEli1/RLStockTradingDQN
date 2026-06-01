"""Tkinter GUI that delegates all business logic to the SDK."""

import threading
import tkinter as tk
from tkinter import ttk

from dqn_trader.sdk.sdk import TradingSDK


class TraderApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("DQN Trader SDK")
        self.geometry("720x420")
        self.sdk = TradingSDK()
        self.ticker = tk.StringVar(value=self.sdk.config["data"]["ticker"])
        self.output = tk.StringVar(value="Ready")
        self._build()

    def _build(self) -> None:
        frame = ttk.Frame(self, padding=12)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Ticker").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.ticker, width=12).grid(row=0, column=1, sticky="w")
        ttk.Button(frame, text="Prepare Data", command=self._prepare).grid(row=1, column=0, pady=8)
        ttk.Button(frame, text="Train Dueling DQN", command=self._train).grid(row=1, column=1, pady=8)
        ttk.Button(frame, text="Backtest", command=self._backtest).grid(row=1, column=2, pady=8)
        ttk.Button(frame, text="Predict", command=self._predict).grid(row=1, column=3, pady=8)
        ttk.Label(frame, textvariable=self.output, wraplength=660).grid(row=2, column=0, columnspan=4, sticky="w")

    def _prepare(self) -> None:
        self._run(lambda: self.sdk.prepare_data(self.ticker.get()), "Data prepared")

    def _train(self) -> None:
        self._run(lambda: self.sdk.train(self.ticker.get()), "Training completed")

    def _backtest(self) -> None:
        self._run(lambda: self.sdk.backtest(self.ticker.get()), "Backtest completed")

    def _predict(self) -> None:
        self._run(lambda: self.sdk.predict_latest(self.ticker.get()), "Prediction completed")

    def _run(self, func, success: str) -> None:
        def worker() -> None:
            try:
                result = func()
                self.output.set(f"{success}: {result}")
            except Exception as exc:
                self.output.set(f"Error: {exc}")

        threading.Thread(target=worker, daemon=True).start()


def launch_gui() -> None:
    TraderApp().mainloop()
