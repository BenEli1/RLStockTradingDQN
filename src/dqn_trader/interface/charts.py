"""Matplotlib chart helpers for the Tkinter interface."""

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class ChartPanel:
    def __init__(self, parent, title: str) -> None:
        self.figure = Figure(figsize=(7.2, 3.8), dpi=100)
        self.axis = self.figure.add_subplot(111)
        self.secondary_axis = None
        self.axis.set_title(title)
        self.canvas = FigureCanvasTkAgg(self.figure, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _clear(self) -> None:
        if self.secondary_axis is not None:
            self.secondary_axis.remove()
            self.secondary_axis = None
        self.axis.clear()

    def draw_lines(self, series: dict[str, list[float]], title: str, ylabel: str) -> None:
        self._clear()
        self.axis.set_title(title)
        self.axis.set_ylabel(ylabel)
        self.axis.grid(True, alpha=0.25)
        for label, values in series.items():
            if values:
                self.axis.plot(values, label=label)
        if any(series.values()):
            self.axis.legend(loc="best")
        self.figure.tight_layout()
        self.canvas.draw()

    def draw_dual_axis(
        self,
        left_series: dict[str, list[float]],
        right_series: dict[str, list[float]],
        title: str,
        left_ylabel: str,
        right_ylabel: str,
    ) -> None:
        self._clear()
        self.secondary_axis = self.axis.twinx()
        self.axis.set_title(title)
        self.axis.set_xlabel("Episode")
        self.axis.set_ylabel(left_ylabel)
        self.secondary_axis.set_ylabel(right_ylabel)
        self.axis.grid(True, alpha=0.25)

        lines = []
        for label, values in left_series.items():
            if values:
                lines.extend(self.axis.plot(values, label=label, color="#2563eb", marker="o"))
        for label, values in right_series.items():
            if values:
                lines.extend(
                    self.secondary_axis.plot(
                        values, label=label, color="#f97316", marker="s", alpha=0.85
                    )
                )
        if lines:
            self.axis.legend(lines, [line.get_label() for line in lines], loc="best")
        self.figure.tight_layout()
        self.canvas.draw()

    def draw_empty(self, message: str) -> None:
        self._clear()
        self.axis.text(0.5, 0.5, message, ha="center", va="center", wrap=True)
        self.axis.set_xticks([])
        self.axis.set_yticks([])
        self.figure.tight_layout()
        self.canvas.draw()
