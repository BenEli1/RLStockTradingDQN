"""Matplotlib chart helpers for the Tkinter interface."""

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class ChartPanel:
    def __init__(self, parent, title: str) -> None:
        self.figure = Figure(figsize=(7.2, 3.8), dpi=100)
        self.axis = self.figure.add_subplot(111)
        self.axis.set_title(title)
        self.canvas = FigureCanvasTkAgg(self.figure, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def draw_lines(self, series: dict[str, list[float]], title: str, ylabel: str) -> None:
        self.axis.clear()
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

    def draw_empty(self, message: str) -> None:
        self.axis.clear()
        self.axis.text(0.5, 0.5, message, ha="center", va="center", wrap=True)
        self.axis.set_xticks([])
        self.axis.set_yticks([])
        self.figure.tight_layout()
        self.canvas.draw()
