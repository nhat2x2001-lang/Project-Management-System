# app/theme.py — Color palette, font constants, and ttk style bootstrap for Project Uno.

from tkinter import ttk

# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------

# Sidebar
SIDEBAR_BG       = "#1a2744"
SIDEBAR_ACTIVE   = "#2d4a7a"
SIDEBAR_HOVER    = "#243459"
SIDEBAR_TEXT     = "#ffffff"
SIDEBAR_ICON     = "#90aecb"
SIDEBAR_BORDER   = "#0f1a2e"

# Main content area
MAIN_BG          = "#f0f4f8"
CONTENT_BG       = "#f0f4f8"

# Cards
CARD_BG          = "#ffffff"
CARD_BORDER      = "#e2e8f0"
CARD_SHADOW      = "#d0d7e2"

# Typography
TEXT_DARK        = "#1a3a5c"
TEXT_BODY        = "#374151"
TEXT_MUTED       = "#6b7a8d"
TEXT_WHITE       = "#ffffff"

# Brand / accent
PRIMARY          = "#1f4e79"
ACCENT           = "#2563eb"

# Semantic colours used in KPI cards
COLOR_BLUE       = "#2563eb"
COLOR_GREEN      = "#16a34a"
COLOR_ORANGE     = "#f59e0b"
COLOR_RED        = "#dc2626"
COLOR_PURPLE     = "#7c3aed"
COLOR_TEAL       = "#0d9488"

# Chart palette (matches cards)
CHART_PALETTE = [COLOR_BLUE, COLOR_GREEN, COLOR_ORANGE, COLOR_RED, COLOR_PURPLE,
                 COLOR_TEAL, "#db2777", "#0891b2", "#65a30d", "#b45309"]

# ---------------------------------------------------------------------------
# Font helpers
# ---------------------------------------------------------------------------

FONT_FAMILY  = "Segoe UI"

def font(size: int = 10, weight: str = "normal") -> tuple:
    return (FONT_FAMILY, size, weight)

F_H1    = font(18, "bold")
F_H2    = font(14, "bold")
F_H3    = font(12, "bold")
F_BODY  = font(10)
F_SMALL = font(9)
F_BOLD  = font(10, "bold")


# ---------------------------------------------------------------------------
# ttk style configuration
# ---------------------------------------------------------------------------

def apply_styles(style: ttk.Style) -> None:
    """Apply the Project Uno theme to all ttk widgets."""
    style.theme_use("default")

    style.configure("TFrame",            background=MAIN_BG)
    style.configure("TLabel",            background=MAIN_BG, foreground=TEXT_DARK,
                                         font=F_BODY)
    style.configure("TLabelframe",       background=MAIN_BG, foreground=TEXT_DARK,
                                         borderwidth=1, relief="solid")
    style.configure("TLabelframe.Label", background=MAIN_BG, foreground=PRIMARY,
                                         font=F_H3)
    style.configure("TNotebook",         background=MAIN_BG)
    style.configure("TNotebook.Tab",     font=F_BOLD, padding=[12, 6])

    style.configure("Treeview",
                    background=CARD_BG,
                    foreground=TEXT_BODY,
                    fieldbackground=CARD_BG,
                    font=F_BODY,
                    rowheight=26)
    style.configure("Treeview.Heading",
                    font=F_BOLD,
                    foreground=TEXT_DARK,
                    background="#eaf0f8",
                    relief="flat")
    style.map("Treeview",
              background=[("selected", ACCENT)],
              foreground=[("selected", TEXT_WHITE)])
    style.map("Treeview.Heading", relief=[("active", "flat")])

    style.configure("TButton",
                    font=F_BOLD,
                    padding=[10, 5],
                    background=PRIMARY,
                    foreground=TEXT_WHITE,
                    relief="flat",
                    borderwidth=0)
    style.map("TButton",
              background=[("active", ACCENT), ("pressed", "#163a61")],
              foreground=[("active", TEXT_WHITE)])

    style.configure("TEntry",
                    font=F_BODY,
                    fieldbackground=CARD_BG,
                    foreground=TEXT_BODY,
                    relief="solid",
                    borderwidth=1)
    style.configure("TCombobox",
                    font=F_BODY,
                    fieldbackground=CARD_BG,
                    foreground=TEXT_BODY)

    style.configure("TSeparator",  background=CARD_BORDER)
    style.configure("TScrollbar",  troughcolor=MAIN_BG, background=CARD_BORDER,
                                   arrowcolor=TEXT_MUTED)

    # Flat section header label (used in sidebar / panel headers)
    style.configure("Header.TLabel", font=F_H2, foreground=TEXT_DARK, background=MAIN_BG)
