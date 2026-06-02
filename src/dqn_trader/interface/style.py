"""Tkinter style setup for the dashboard UI."""

import tkinter as tk
from tkinter import ttk


def apply_dashboard_style(root: tk.Tk) -> None:
    style = ttk.Style(root)
    style.theme_use("clam")
    root.configure(bg="#f4f6f8")
    style.configure(".", font=("Segoe UI", 10))
    style.configure("TFrame", background="#f4f6f8")
    style.configure("TLabelframe", background="#ffffff", bordercolor="#d0d7de")
    style.configure("TLabelframe.Label", background="#ffffff", font=("Segoe UI", 11, "bold"))
    style.configure("TNotebook", background="#f4f6f8", borderwidth=0)
    style.configure("TNotebook.Tab", padding=(14, 6), font=("Segoe UI", 10, "bold"))
    style.configure("Status.TLabel", padding=6, background="#eef2f6")
    style.configure("TButton", padding=6)
    style.configure(
        "Accent.TButton",
        padding=7,
        background="#2563eb",
        foreground="#ffffff",
        bordercolor="#1d4ed8",
        font=("Segoe UI", 10, "bold"),
    )
    style.map(
        "Accent.TButton",
        background=[("active", "#1d4ed8"), ("pressed", "#1e40af")],
        foreground=[("disabled", "#dbeafe"), ("!disabled", "#ffffff")],
    )
    style.configure(
        "Primary.TButton",
        padding=8,
        background="#111827",
        foreground="#ffffff",
        bordercolor="#111827",
        font=("Segoe UI", 10, "bold"),
    )
    style.map(
        "Primary.TButton",
        background=[("active", "#374151"), ("pressed", "#030712")],
        foreground=[("disabled", "#e5e7eb"), ("!disabled", "#ffffff")],
    )
