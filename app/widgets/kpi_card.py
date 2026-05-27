# app/widgets/kpi_card.py — KPI summary card widget.

import tkinter as tk
from tkinter import ttk

from app import theme


class KPICard(tk.Frame):
    """A card widget displaying a KPI metric.

    Shows:
    - A left-side accent bar (colour-coded per metric)
    - A large value number
    - A descriptive label below
    - An icon character at the top-right

    Parameters
    ----------
    parent : widget
    label : str       — Metric title (e.g. "Total Tasks")
    value : str | int — Initial value to display
    icon  : str       — Unicode character used as icon (e.g. "📋")
    accent_color : str — Hex colour for the left accent bar
    """

    def __init__(self, parent, label: str, value="—",
                 icon: str = "●", accent_color: str = theme.COLOR_BLUE, **kwargs):
        super().__init__(parent,
                         bg=theme.CARD_BG,
                         highlightbackground=theme.CARD_BORDER,
                         highlightthickness=1,
                         **kwargs)

        self._accent_color = accent_color
        self._label_text   = label

        # Left accent bar
        accent_bar = tk.Frame(self, bg=accent_color, width=5)
        accent_bar.pack(side="left", fill="y")

        # Content area
        body = tk.Frame(self, bg=theme.CARD_BG, padx=14, pady=12)
        body.pack(side="left", fill="both", expand=True)

        # Top row: label + icon
        top_row = tk.Frame(body, bg=theme.CARD_BG)
        top_row.pack(fill="x")

        self._label_widget = tk.Label(
            top_row, text=label.upper(),
            bg=theme.CARD_BG, fg=theme.TEXT_MUTED,
            font=(theme.FONT_FAMILY, 8, "bold")
        )
        self._label_widget.pack(side="left")

        icon_label = tk.Label(
            top_row, text=icon,
            bg=theme.CARD_BG, fg=accent_color,
            font=(theme.FONT_FAMILY, 14)
        )
        icon_label.pack(side="right")

        # Value (big number)
        self._value_widget = tk.Label(
            body, text=str(value),
            bg=theme.CARD_BG, fg=TEXT_DARK_OR_ACCENT(accent_color),
            font=(theme.FONT_FAMILY, 26, "bold")
        )
        self._value_widget.pack(anchor="w", pady=(4, 0))

    def update_value(self, value) -> None:
        """Update the displayed value."""
        self._value_widget.config(text=str(value))


def TEXT_DARK_OR_ACCENT(accent_color: str) -> str:
    """Return TEXT_DARK for most colours; keeps readability."""
    return theme.TEXT_DARK
