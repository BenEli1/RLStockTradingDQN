"""Generate README demonstration images without claiming real experiment results."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ASSETS = Path("assets")


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    name = "arialbd.ttf" if bold else "arial.ttf"
    try:
        return ImageFont.truetype(name, size)
    except OSError:
        return ImageFont.load_default()


def draw_dashboard_preview() -> None:
    image = Image.new("RGB", (1280, 820), "#f4f6f8")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1280, 72), fill="#1f2937")
    draw.text((34, 20), "DQN Trader SDK - Tkinter Dashboard", fill="white", font=font(28, True))
    draw.rectangle((28, 96, 292, 790), fill="#ffffff", outline="#d0d7de")
    draw.text((48, 122), "Run Controls", fill="#111827", font=font(22, True))
    for idx, label in enumerate(
        [
            "Ticker: AAPL",
            "Episodes: 5",
            "Prepare Data",
            "Train",
            "Backtest",
            "Predict",
            "Run Full Pipeline",
        ]
    ):
        y = 172 + idx * 58
        color = "#e5edf7" if idx < 2 else "#111827" if idx == 6 else "#2563eb"
        text_color = "#111827" if idx < 2 else "#ffffff"
        draw.rounded_rectangle((48, y, 254, y + 42), radius=8, fill=color, outline="#c9d3df")
        draw.text((66, y + 11), label, fill=text_color, font=font(16, idx >= 2))
    draw.text((48, 616), "Summary", fill="#111827", font=font(18, True))
    draw.multiline_text(
        (48, 646),
        "AAPL 2020 -> 2023\nClose: 75.09 -> 129.93\nFeature rows: 723\nPrediction: HOLD",
        fill="#374151",
        font=font(15),
        spacing=8,
    )
    draw.rectangle((320, 96, 1240, 790), fill="#ffffff", outline="#d0d7de")
    tabs = ["Dashboard", "Run Log"]
    for i, tab in enumerate(tabs):
        x = 338 + i * 150
        draw.rounded_rectangle((x, 116, x + 136, 154), radius=8, fill="#e5edf7", outline="#c9d3df")
        draw.text((x + 16, 126), tab, fill="#111827", font=font(15, True))

    panels = [
        (354, 182, 772, 430, "Market Data"),
        (790, 182, 1208, 430, "Training"),
        (354, 454, 1208, 742, "Backtest"),
    ]
    for x1, y1, x2, y2, title in panels:
        draw.rectangle((x1, y1, x2, y2), fill="#fbfdff", outline="#d0d7de")
        draw.text((x1 + 18, y1 + 16), title, fill="#111827", font=font(18, True))

    x_values = np.linspace(0, 1, 180)
    market = 0.45 + 0.18 * np.sin(8 * x_values) + 0.18 * x_values
    reward = 0.55 + 0.12 * np.sin(15 * x_values)
    backtest_a = 0.45 + 0.15 * np.sin(10 * x_values) + 0.22 * x_values
    backtest_b = 0.42 + 0.12 * np.sin(9 * x_values) + 0.13 * x_values
    market_points = [
        (376 + int(x * 360), 392 - int(y * 170)) for x, y in zip(x_values, market, strict=True)
    ]
    reward_points = [
        (812 + int(x * 360), 392 - int(y * 170)) for x, y in zip(x_values, reward, strict=True)
    ]
    backtest_points_a = [
        (380 + int(x * 790), 702 - int(y * 210)) for x, y in zip(x_values, backtest_a, strict=True)
    ]
    backtest_points_b = [
        (380 + int(x * 790), 702 - int(y * 210)) for x, y in zip(x_values, backtest_b, strict=True)
    ]
    draw.line(market_points, fill="#2563eb", width=4)
    draw.line(reward_points, fill="#f97316", width=4)
    draw.line(backtest_points_a, fill="#2563eb", width=4)
    draw.line(backtest_points_b, fill="#f97316", width=3)
    draw.text((378, 232), "Close price", fill="#4b5563", font=font(15))
    draw.text((814, 232), "Reward + mean loss", fill="#4b5563", font=font(15))
    draw.text((378, 504), "DQN vs Buy-and-Hold equity", fill="#4b5563", font=font(15))
    draw.rectangle((0, 790, 1280, 820), fill="#e5e7eb")
    draw.text(
        (34, 798),
        "Controlled preview generated from the current UI layout; run `uv run dqn-trader gui` for the live app.",
        fill="#374151",
        font=font(14),
    )
    image.save(ASSETS / "gui_dashboard_preview.png")


def save_line_plot(path: Path, title: str, ylabel: str, series: dict[str, np.ndarray]) -> None:
    plt.figure(figsize=(9, 4.8), dpi=140)
    for label, values in series.items():
        plt.plot(values, label=label)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("Step")
    plt.grid(True, alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def draw_demo_plots() -> None:
    x = np.arange(160)
    close = 150 + np.cumsum(np.sin(x / 13) * 0.8 + 0.35)
    rewards = np.tanh(np.linspace(-2, 2, 40)) + np.sin(np.linspace(0, 8, 40)) * 0.08
    losses = np.exp(-np.linspace(0, 4, 70)) + 0.03 * np.sin(np.linspace(0, 20, 70))
    dqn = 10000 + np.cumsum(np.sin(x / 11) * 18 + 5)
    hold = 10000 + np.cumsum(np.sin(x / 17) * 10 + 3)
    save_line_plot(
        ASSETS / "demo_market_data.png", "Demo Market Data Chart", "Close Price", {"Close": close}
    )
    figure, (reward_axis, loss_axis) = plt.subplots(2, 1, figsize=(9, 4.8), dpi=140, sharex=True)
    reward_axis.plot(rewards, color="#2563eb", label="Reward")
    reward_axis.set_title("Demo Training Chart")
    reward_axis.set_ylabel("Reward")
    reward_axis.grid(True, alpha=0.25)
    reward_axis.legend()
    loss_axis.plot(losses[: len(rewards)], color="#f97316", label="Mean loss")
    loss_axis.set_xlabel("Episode")
    loss_axis.set_ylabel("Mean loss")
    loss_axis.grid(True, alpha=0.25)
    loss_axis.legend()
    figure.tight_layout()
    figure.savefig(ASSETS / "demo_training_curve.png")
    plt.close(figure)
    save_line_plot(
        ASSETS / "demo_backtest_equity.png",
        "Demo Backtest Equity Chart",
        "Portfolio Value",
        {"DQN": dqn, "Buy-and-Hold": hold},
    )


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    draw_dashboard_preview()
    draw_demo_plots()


if __name__ == "__main__":
    main()
